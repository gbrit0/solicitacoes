from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
import re

User = get_user_model()

class LoginSerializer(serializers.Serializer):
   cpf = serializers.CharField()
   senha = serializers.CharField(write_only=True)

   def validate(self, data):
      cpf = re.sub(r'\D', '', data.get('cpf'))
      senha = data.get('senha')
      user = authenticate(username=cpf, password=senha)

      if user is None:
         raise serializers.ValidationError("Credenciais inválidas.")
      data['user'] = user
      return data


class CadastroSerializer(serializers.ModelSerializer):
   senha = serializers.CharField(write_only=True)

   class Meta:
      model = User
      fields = ['cpf', 'nome', 'email', 'senha', 'role']

   def validate_cpf(self, value):
      cpf = re.sub(r'\D', '', value)
      if User.objects.filter(cpf=cpf).exists():
         raise serializers.ValidationError("CPF já cadastrado.")
      return cpf

   def create(self, validated_data):
      cpf = re.sub(r'\D', '', validated_data.pop('cpf'))
      senha = validated_data.pop('senha')
      id = str(int(User.objects.latest('id').id) + 1).zfill(6)

      user = User.objects.create_user(
         cpf=cpf,
         id=id,
         password=senha,
         **validated_data
      )
      return user
