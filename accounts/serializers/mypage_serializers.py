from django.utils.translation import gettext as _

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from rest_auth.registration.serializers import RegisterSerializer

from board_list.serializers.boardlist_serializers import BoardListSerializer

from accounts.models import Profile
from custom_admin.models import PointLog

from common.validators import NewASCIIUsernameValidator, NicknameValidator


class ProfileSerializer(RegisterSerializer):
    username = serializers.CharField(
        required=True,
        min_length=5,
        max_length=20,
        validators=[UniqueValidator(queryset=Profile.objects.all()), NewASCIIUsernameValidator()],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    nickname = serializers.CharField(
        required=True,
        min_length=1,
        max_length=20,
        validators=[UniqueValidator(queryset=Profile.objects.all()), NicknameValidator()]
    )
    introduction = serializers.CharField(max_length=300, required=False, )
    profile_image = serializers.ImageField(required=False, )
    bookmark = BoardListSerializer(read_only=True, many=True)
    points = serializers.CharField(read_only=True)
    level = serializers.CharField(read_only=True)
    unique_key = serializers.CharField(required=True, )
    gender = serializers.CharField(required=False, )
    birthday = serializers.CharField(required=False, )

    class Meta:
        model = Profile

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['nickname'] = self.validated_data.get('nickname', '')
        data_dict['introduction'] = self.validated_data.get('introduction', '')
        data_dict['profile_image'] = self.validated_data.get('profile_image', '')
        data_dict['unique_key'] = self.validated_data.get('unique_key', '')
        data_dict['gender'] = self.validated_data.get('gender', '')
        data_dict['birthday'] = self.validated_data.get('birthday', '')
        return data_dict


# ?????? ?????? ?????? (???????????? ??????)
class SuperBasicProfileUpdateSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(
        required=True,
        min_length=1,
        max_length=20,
        validators=[UniqueValidator(queryset=Profile.objects.all()), NicknameValidator()]
    )
    introduction = serializers.CharField(max_length=300, required=False, )
    profile_image = serializers.ImageField(required=False, )
    is_superuser = serializers.BooleanField(read_only=True, required=False)

    class Meta:
        model = Profile
        fields = ("nickname", "introduction", "profile_image", "is_superuser")

    def get_is_superuser(self, obj):
        if obj['user'].is_superuser:
            obj['is_superuser'] = True


# ?????? ?????? ?????? (???????????? ?????? ??????)
class BasicProfileUpdateSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(
        required=True,
        min_length=1,
        max_length=20,
        validators=[UniqueValidator(queryset=Profile.objects.all()), NicknameValidator()]
    )
    introduction = serializers.CharField(max_length=300, required=False, )
    profile_image = serializers.ImageField(required=False, )

    class Meta:
        model = Profile
        fields = ("nickname", "introduction", "profile_image")


# ???????????? ?????????
class GetBookmarkSerializer(serializers.ModelSerializer):
    bookmark = BoardListSerializer(read_only=True, many=True)

    class Meta:
        model = Profile
        fields = ("bookmark",)


# ???????????? ?????????
class PostBookmarkSerializer(serializers.ModelSerializer):
    bookmark = serializers.CharField()

    class Meta:
        model = Profile
        fields = ("bookmark",)


# ????????? ????????? ?????? ?????? ?????? ??? ?????????
class ScoreSerializer(serializers.ModelSerializer):
    nickname = serializers.CharField(
        required=True,
        min_length=1,
        max_length=20,
        validators=[UniqueValidator(queryset=Profile.objects.all())]
    )
    board_write = serializers.IntegerField(read_only=True)
    reply_write = serializers.IntegerField(read_only=True)
    rereply_write = serializers.IntegerField(read_only=True)
    total = serializers.IntegerField(read_only=True)

    class Meta:
        model = Profile
        fields = ("nickname", "board_write", "reply_write", "rereply_write", "total")


# ????????? ??????????????? ??? ?????? ??????
class MyPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PointLog
        fields = ("id", "kind", "information", "points", "created_at",)


# ?????? ????????? ???(?????????)
class MyBoardSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(read_only=True)
    body = serializers.CharField(read_only=True)
    board_url = serializers.SerializerMethodField(read_only=True)
    reply_count = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(format='%Y/%m/%d %H:%M', read_only=True)

    def get_board_url(self, obj):
        return {'board_url': obj.board_url, 'board_name': obj.board_name, 'division': obj.division}


# ?????? ??? ?????? ??????(?????????)
class MyReplySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    board_post_id_id = serializers.IntegerField(read_only=True)
    body = serializers.CharField(read_only=True)
    reply_image = serializers.ImageField(read_only=True)
    # ????????????
    recommend_count = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(format='%Y/%m/%d %H:%M', read_only=True)


# ?????? ??? ?????? ????????? ???????????????(accounts.views) serializer
class MyreReplySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    board_post_id_id = serializers.IntegerField(read_only=True)
    reply_id_id = serializers.IntegerField(read_only=True)
    body = serializers.CharField(read_only=True)
    rereply_image = serializers.ImageField(read_only=True)

    # ????????????
    recommend_count = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(format='%Y/%m/%d %H:%M', read_only=True)