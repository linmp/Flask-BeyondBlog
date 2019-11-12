from . import main


# 发表博客
@main.route("/blog/article", methods=["POST"])
def post_blog_article():
    pass


# 获取博客详情
@main.route("/blog/article/detail", methods=["POST"])
def get_article_detail():
    pass
