from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import Tree, TreeNode, NodeRelation
from django.urls import reverse
import json
# Create your tests here.
class TreeNodeTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='12345')
        self.tree = Tree.objects.create(name='Test Tree', owner=self.user)
        self.node1 = TreeNode.objects.create(name='Node 1', tree=self.tree)
        self.node2 = TreeNode.objects.create(name='Node 2', tree=self.tree)

    def test_get_ancestors_method(self):
        ancestor_node = TreeNode.objects.create(name='Ancestor Node', tree=self.tree)
        self.node1.parents.add(ancestor_node)
        ancestors = self.node1.get_ancestors()
        self.assertIn(ancestor_node, ancestors)

    def test_get_descendants_method(self):
        descendant_node = TreeNode.objects.create(name='Descendant Node', tree=self.tree)
        self.node1.children.add(descendant_node)
        descendants = self.node1.get_descendants()
        self.assertIn(descendant_node, descendants)

class NodeRelationTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='12345')
        self.tree = Tree.objects.create(name='Test Tree', owner=self.user)
        self.node1 = TreeNode.objects.create(name='Node 1', tree=self.tree)
        self.node2 = TreeNode.objects.create(name='Node 2', tree=self.tree)

    def test_unique_together_constraint(self):
        try:
            NodeRelation.objects.create(tree=self.tree, parent=self.node1, child=self.node2)
            NodeRelation.objects.create(tree=self.tree, parent=self.node1, child=self.node2)
        except ValidationError as e:
            self.assertTrue(isinstance(e, ValidationError))
            self.assertEqual(e.message, "A NodeRelation with this tree, parent and child already exists.")


class IndexViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.client.login(username='testuser', password='12345')

    def test_index_view_with_login(self):
        response = self.client.get(reverse('focus_tree:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'focus_tree/index.html')

    def test_create_tree_view(self):
        response = self.client.post(reverse('focus_tree:endpoint_create_tree'), {'tree_name': 'New Tree'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Tree.objects.filter(name='New Tree', owner=self.user).exists())

    def test_tree_editer_view(self):
        tree = Tree.objects.create(name='Test Tree', owner=self.user)
        response = self.client.get(reverse('focus_tree:tree_editer', args=[tree.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'focus_tree/tree_editer.html')

class SaveOneTest(TestCase):
    '''
    name = models.CharField(max_length=100)
    tree = models.ForeignKey(Tree, related_name='nodes', on_delete=models.CASCADE, null=True)
    image = models.ImageField(null=True, blank=True, upload_to='focus_tree/images/%Y/%m/%d')
    main_text = models.CharField(max_length=10000, default='')
    position_x = models.IntegerField(default=0)
    position_y = models.IntegerField(default=0)
    '''
    def setUp(self):
        self.user = User.objects.create_user(username='test_user', password='12345')
        self.tree = Tree.objects.create(name='Test Tree', owner=self.user)
        self.node_data = {
            'name': 'Test Node',
            'main_text': 'Test Content',
            'image': 'test.png',
        }

    def test_save_one_success(self):
        url = reverse('focus_tree:ajax_save_one', args=[self.tree.id])
        response = self.client.post(url, self.node_data, format='json')

        self.assertEqual(response.status_code, 302)  # Check if redirect status code is returned
        self.assertEqual(TreeNode.objects.filter(name='Test Node').count(), 1)  # Check if node is created in the database

    def test_save_one_invalid_data(self):
        # Providing incomplete data to the form to simulate invalid data
        invalid_data = {
            'name': 'Incomplete Node'
        }
        url = reverse('focus_tree:ajax_save_one', args=[self.tree_id])
        response = self.client.post(url, invalid_data, format='json')

        self.assertEqual(response.status_code, 302)  # Check if redirect status code is returned
        self.assertEqual(TreeNode.objects.filter(name='Incomplete Node').count(), 0)  # Check that node is not created with incomplete data

class SaveAllTestCase(TestCase):
    
    def test_save_all_with_valid_data(self):
        # Prepare test data
        tree_node = TreeNode.objects.create(id=1, position_x=100, position_y=200)
    
        # Prepare request
        data = [{
            'id': 1,
            'x': 150,
            'y': 250
        }]
        response = self.client.post(reverse('focus_tree:ajax_save_all', args=(tree_node.id,)), data=data, content_type='application/json')
    
        # Check if position got updated
        updated_node = TreeNode.objects.get(id=1)
        self.assertEqual(updated_node.position_x, 150)
        self.assertEqual(updated_node.position_y, 250)
    
        # Check response
        self.assertRedirects(response, expected_url=reverse('focus_tree:tree_editer', args=(tree_node.id,)), status_code=302, target_status_code=200)
    
    def test_save_all_with_invalid_data(self):
        # Prepare request with malformed data
        data = [{'invalid_key': 'value'}]
        response = self.client.post(reverse('focus_tree:ajax_save_all', args=(1,)), data=data, content_type='application/json')
    
        # Check if no node got updated
        nodes = TreeNode.objects.all()
        for node in nodes:
            self.assertNotEqual(node.position_x, 150)
            self.assertNotEqual(node.position_y, 250)
    
        # Check response and logs for error message
        self.assertContains(response, text="Malformed data!", status_code=200)

class TestSaveRelationship(TestCase):
    def setUp(self):
        self.tree = Tree.objects.create()  # Create a tree object for testing

    def test_save_relationship_POST_request(self):
        url = reverse('focus_tree:endpoint_save_relationship', args=[self.tree.pk])
        data = [
            {'parent': 1, 'child': 2},
            {'parent': 1, 'child': 3},
        ]
        response = self.client.post(url, json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json())  # Check if the response contains data

        # Check if the relationships were saved correctly
        master_tree = Tree.objects.get(pk=self.tree.pk)
        parent_node_1 = TreeNode.objects.get(node_id=1)
        
        child_node_2 = TreeNode.objects.get(node_id=2)
        child_node_3 = TreeNode.objects.get(node_id=3)

        self.assertTrue(NodeRelation.objects.filter(tree=master_tree, parent=parent_node_1, child=child_node_2).exists())
        self.assertTrue(NodeRelation.objects.filter(tree=master_tree, parent=parent_node_1, child=child_node_3).exists())

        # Check if the response data is as expected
        nodes = TreeNode.objects.filter(tree=self.tree)
        response_data = response.json()

        for node in nodes:
            self.assertIn(str(node.id), response_data)
            self.assertEqual(response_data[str(node.id)]['id'], node.id)
            # Add more assertions for other fields as needed

class TestViews(TestCase):
    def setUp(self):
        self.tree_id = 1

    def test_delete_edge(self):
        response = self.client.post(reverse('focus_tree:endpoint_delete_all_edge', kwargs={'id': self.tree_id}))
        self.assertEqual(response.status_code, 200)

        # Edge가 삭제되었는지 확인하는 코드
        self.assertEqual(NodeRelation.objects.filter(tree=self.tree_id).count(), 0)

    def test_delete_node(self):
        response = self.client.post(reverse('focus_tree:endpoint_delete_all_node', kwargs={'id': self.tree_id}))
        self.assertEqual(response.status_code, 200)

        # Node가 삭제되었는지 확인하는 코드
        self.assertEqual(TreeNode.objects.filter(tree=self.tree_id).count(), 0)

    def test_download_tree_html(self):
        nodes = [{"id": 1, "name": "Node 1"}, {"id": 2, "name": "Node 2"}]
        json_data = json.dumps(nodes)
        response = self.client.post(reverse('focus_tree:endpoint_download_tree_html'), data=json_data, content_type='application/json')
        self.assertEqual(response.status_code, 200)

        # 생성된 HTML 파일을 다운로드 했는지 확인하는 코드
        self.assertTrue(response.has_header('Content-Disposition'))
