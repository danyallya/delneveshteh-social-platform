import json
from utils.calverter import gregorian_to_jalali

__author__ = 'M.Y'
from django.template.defaultfilters import linebreaksbr


class CommentHandler:
    def __init__(self, comments):
        self.comments = list(comments)
        self.comments_children = {}

    # def render(self):
    #     self.__create_comment_tree()
    #
    #     root_comments = filter(lambda comment: not comment.reply_to_id, self.comments)
    #
    #     return self.__render_comments(root_comments)

    def __create_comment_tree(self):
        for comment in self.comments:
            children_list = list(filter(lambda child: child.reply_to_id == comment.id, self.comments))
            self.comments_children[str(comment.id)] = children_list

    def __render_comments(self, comments):
        if not comments:
            return ""

        res = '<ul id="comments-ul">'

        for comment in comments:
            res += '<li class="comment-item"  data-comment-id="%s">' % comment.id

            res += linebreaksbr(comment.text)

            res += ' <a href="javascript:void(0)" class="comment-reply" title="پاسخ">پاسخ</a>'
            res += '<div class="reply-form hidden"></div><br/>'

            children_list = self.comments_children[str(comment.id)]

            res += self.__render_comments(children_list)

            res += "</li>"

        res += '</ul>'

        return res

    @staticmethod
    def render_comment_item(comment):
        res = '<li class="comment-item"  data-comment-id="%s"><div class="comment-text">' % comment.id

        if comment.reply_to_id:
            res += '<span class="comment-parent-right"></span><span class="comment-parent">%s</span><br/> ' % \
                   linebreaksbr(comment.reply_to.text[:20])

        res += '<span class="comment-name">%s:</span> ' % str(comment.user or comment.user_name or "ناشناس")

        res += linebreaksbr(comment.text)

        res += ' <a href="javascript:void(0)" class="comment-reply" title="پاسخ">پاسخ</a>'
        res += '<div class="reply-form hidden"></div><br/>'

        res += '</div><img src="/static/images/page/person.jpg" class="comment-image"/>'

        res += "</li>"
        return res

    def render_comments_inline(self):
        self.__create_comment_tree()
        root_comments = filter(lambda comment: not comment.reply_to_id, self.comments)

        res = '<ul id="comments-ul">'
        res += self.render_comments_items(root_comments)
        res += '</ul>'

        return res

    def render_comments_items(self, comments):
        if not comments:
            return ""

        res = ""
        for comment in comments:
            res += CommentHandler.render_comment_item(comment)

            children_list = self.comments_children[str(comment.id)]

            res += self.render_comments_items(children_list)

        return res

    def render_comments_json(self):
        self.__create_comment_tree()
        root_comments = filter(lambda comment: not comment.reply_to_id, self.comments)

        res = self.render_comments_json_items(root_comments)

        return json.dumps(res)

    def render_comments_json_items(self, comments):
        if not comments:
            return []

        res = []
        for comment in comments:
            children_list = self.comments_children[str(comment.id)]
            item = {'i': comment.id, 'l': comment.like_count, 'u': str(comment.user), 't': linebreaksbr(comment.text),
                    'd': gregorian_to_jalali(comment.created_on), 'c': self.render_comments_json_items(children_list)}

            res.append(item)

        return res
