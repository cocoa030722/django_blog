from django.urls import path

from . import views
app_name = "focus_tree"
urlpatterns = [
    path("", views.index, name="index"),
    path("<int:id>", views.tree_editer, name="tree_editer"),
    path("ajax/save-all/<int:id>", views.save_all, name="ajax_save_all"),
    path("ajax/save-one/<int:id>", views.save_one, name="ajax_save_one"),
    path("endpoint/create-tree", views.create_tree, name="endpoint_create_tree"),
    path("endpoint/save-relationship/<int:id>", views.save_relationship, name="endpoint_save_relationship"),
    path("endpoint/delete-all-edge/<int:id>", views.delete_edge, name="endpoint_delete_all_edge"),
    path("endpoint/delete-all-node/<int:id>", views.delete_node, name="endpoint_delete_all_node"),
    path("endpoint/download-tree-html", views.download_tree_html, name="endpoint_download_tree_html"),
]