from math import ceil

from django.db.models import Q
from django.http import Http404
from django.shortcuts import render, redirect , reverse
from django.views.generic import View
from django.core.paginator import Paginator

from . import models, forms
from users import models as user_models


def go_conversation(request, a_pk, b_pk):
    user_one = user_models.User.objects.get_or_none(pk=a_pk)
    user_two = user_models.User.objects.get_or_none(pk=b_pk)
    try:
        if user_one is not None and user_two is not None:
            conversation = models.Conversation.objects.get(
                Q(participants=user_one) & Q(participants=user_two)
            )
    except models.Conversation.DoesNotExist:
        conversation = models.Conversation.objects.create()
        conversation.participants.add(user_one, user_two)

    return redirect(reverse("conversations:detail", kwargs={"pk":conversation.pk}))


class ConversationDetailView(View):

    def get(self, *args, **kwargs):
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)

        # 대화 총 갯수
        total_message_count = conversation.messages.count()


        page_size = int(10)
        page = self.request.GET.get("page")
        page = int(page or 1)
        counting = page_size * page
        limit = total_message_count - counting
        page_count = ceil(conversation.messages.count() / page_size)
        print("page_count : ", page_count)
        print("page : ", page, ", counting : ", counting,", limit : ", limit)

        try:
            conversations = conversation.messages.all()[limit:]
            user_id = conversation.participants.all()
            for user in user_id:
                if user != self.request.user:
                    the_other_user = user

        except:
            conversations = conversation.messages.all
            user_id = conversation.participants.all()
            for user in user_id:
                if user != self.request.user:
                    the_other_user = user

        if not conversations:
            raise Http404()

        return render(self.request, "conversations/conversation_detail.html", {
            "conversations":conversations,
            'page':page,"page_range":range(1,page_count+1),
            "the_other_user":the_other_user,
        })

    def post(self, *args, **kwargs):
        message = self.request.POST.get('message', None)
        pk = kwargs.get("pk")
        conversation = models.Conversation.objects.get_or_none(pk=pk)
        if not conversation:
            raise Http404()

        if message is not None:
            models.Message.objects.create(
                message=message,
                user=self.request.user,
                conversation=conversation,
            )
        return redirect(reverse("conversations:detail", kwargs={"pk":pk}))



