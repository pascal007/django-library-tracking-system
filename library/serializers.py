import datetime

from rest_framework import serializers
from .models import Author, Book, Member, Loan
from django.contrib.auth.models import User

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source='author', write_only=True
    )

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'author_id', 'isbn', 'genre', 'available_copies']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class MemberSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True
    )

    class Meta:
        model = Member
        fields = ['id', 'user', 'user_id', 'membership_date']

class LoanSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), source='book', write_only=True
    )
    member = MemberSerializer(read_only=True)
    member_id = serializers.PrimaryKeyRelatedField(
        queryset=Member.objects.all(), source='member', write_only=True
    )

    class Meta:
        model = Loan
        fields = ['id', 'book', 'book_id', 'member', 'member_id', 'loan_date', 'return_date', 'is_returned']


class ExtendDueDateSerializer(serializers.Serializer):
    additional_days = serializers.IntegerField(min_value=1, required=True)
    loan = serializers.PrimaryKeyRelatedField(queryset=Loan.objects.all(), required=True)

    def validate(self, attrs):
        # if attrs['due_date'] < datetime.datetime.now().date():
        #     raise serializers.ValidationError('Date must not be before today')
        # if attrs['due_date'] < attrs['loan'].due_date:
        #     raise serializers.ValidationError('You can only extend due date')

        if attrs['loan'].due_date < datetime.datetime.date():
            raise serializers.ValidationError('Loan already overdue')
        return attrs

    def create(self, validated_data):
        loan = validated_data.get('loan')
        loan.due_date = loan.due_date + datetime.timedelta(days=validated_data.get('additional_days'))
        loan.save()

        return loan