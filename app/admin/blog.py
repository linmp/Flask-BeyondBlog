from . import admin
from app.utils.tool import admin_login_required


# 发表博客
@admin.route("/blog/article", methods=["POST"])
@admin_login_required
def post_blog_article():
    """
    title
    content
    summary
    logo
    author_id
    :return: 
    """
    pass
    


# 获取博客详情
@admin.route("/blog/article/detail", methods=["GET"])
def get_article_detail():
    pass


# 删除博客
@admin.route("/blog/article", methods=["DELETE"])
@admin_login_required
def delete_blog_article():
    pass
