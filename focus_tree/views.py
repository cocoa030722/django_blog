import json
import re
import string
import random
from pathlib import Path
import datetime

from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, TemplateView
from django.template import Context, Template
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required

from .models import TreeNode, NodeRelation, Tree
from .forms import NodeForm, TreeForm

# Create your views here.
    
@login_required(login_url='/common/login')
def index(request):
    trees = Tree.objects.filter(owner=request.user)
    form = TreeForm()
    context_dict = {'trees':trees, 'form': form}
    return render(request, 'focus_tree/index.html', context_dict)

def create_tree(request):
    if request.method == "POST":
        form = TreeForm(request.POST)
        if form.is_valid():
            # 폼 데이터 처리
            tree_name = form.cleaned_data['tree_name']

            new_tree = Tree.objects.create(
                name = tree_name,
                owner = request.user,
            )

            return redirect('focus_tree:tree_editer', id=new_tree.id)
            
def tree_editer(request, id):
    tree = Tree.objects.get(pk=id)
    nodes = TreeNode.objects.filter(tree=id)
    
    send_data = {node.id: {
        'id': node.id,
        'image': node.image.url if node.image else '',
        'name': node.name, 
        'main_text': node.main_text,
        'children': [child.id for child in node.children.all()],
        'position_x':node.position_x, 
        'position_y':node.position_y,} for node in nodes
    }
    form = NodeForm()
    
    context_dict = {'nodes':send_data,
                    'form':form,
                    'tree':tree
                   }
    return render(request, 'focus_tree/tree_editer.html', context_dict)

def save_all(request, id):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        try:
            for data in json_data:
                print(data)
                #프론트가 좌표를 숫자로 줄 거라고 전제하고 그냥 씀
                if TreeNode.objects.filter(id=data['id']).exists():
                    node = TreeNode.objects.get(id=data['id'])
                    node.position_x = data['x']
                    node.position_y = data['y']
                    node.save()
        except KeyError:
            print("Malformed data!")
    print("act:save_one")
    return redirect('focus_tree:tree_editer', id=id)

def save_one(request, id):
    # if this is a POST request we need to process the form data
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = NodeForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            node = form.save(commit=False)
            node.tree = Tree.objects.get(pk=id)
            node.save()

    print("act:save_one")
    return redirect('focus_tree:tree_editer', id=id)
    
def save_relationship(request, id):
    send_data = {}
    if request.method == "POST":
        json_data = json.loads(request.body)
        print(json_data)

        # 부모 자식 관계 생성
        for edge in json_data:
            master_tree = Tree.objects.get(pk=id)
            NodeRelation.objects.create(
                tree = master_tree,
                parent = TreeNode.objects.get(id=edge['parent']),
                child = TreeNode.objects.get(id=edge['child']),
            )
        
        nodes = TreeNode.objects.filter(tree=id)
        
        send_data = {node.id: {
            'id': node.id,
            'image': node.image.url if node.image else '',
            'name': node.name, 
            'main_text': node.main_text,
            'children': [child.id for child in node.children.all()],
            'position_x':node.position_x, 
            'position_y':node.position_y,} for node in nodes
        }
    
    return JsonResponse(send_data)

def delete_edge(request, id):
    NodeRelation.objects.filter(tree=id).delete()
    data = {
        "labels": "aigonan1"
    }
    return JsonResponse(data)

def delete_node(request, id):
    TreeNode.objects.filter(tree=id).delete()
    data = {
        "labels": "aigonan2"
    }
    return JsonResponse(data)

def download_tree_html(request):
    json_data = json.loads(request.body)
    print(json_data)
    # 트리의 노드와 간선을 정의
    nodes = json_data

    # HTML 파일 생성
  
    # html_content = generate_tree_html(nodes)
    html_content = render_to_string('focus_tree/download_tree.html', {'nodes': nodes})
    # 현재 날짜와 시간을 포함한 파일명 생성
    filename = f"tree_structure_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.html"

    # 파일을 다운로드할 수 있도록 응답 생성
    response = HttpResponse(html_content, content_type='text/html')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response

