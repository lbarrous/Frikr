from django.contrib.auth.models import User
from rest_framework import serializers

class UserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField() # Solo lectura, no queremos que sea editable
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField()

    def create(self, validated_data):
        """
        Crear una instancia de User a partir de los datos de validated_data, que contienen
        valores deserializados
        :param validated_data: Diccionario con datos de usuario
        :return: Objeto User
        """

        instance = User()
        return self.update(instance, validated_data)


    def update(self, instance, validated_data):
        """
        Actualiza una instancia de User a partir de los datos del ccionario validated_data
        que contiene valores deserializados
        :param instance: Objeto User a actualizar
        :param validated_data: Objeto user actualizado
        :return:
        """
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.last_name = validated_data.get('last_name')
        instance.username = validated_data.get('username')
        instance.email = validated_data.get('email')
        instance.set_password(validated_data.get('password'))
        instance.save()

        return instance

    def validate_username(self, data):
        """
        Valida si existe un usuario con ese username
        """
        user = User.objects.filter(username=data)

        # Si estoy creando (no hay instancia) comprobar si hay usuarios con ese username
        if not self.instance and len(user) != 0:
            raise serializers.ValidationError("Ya existe un usuario con ese nombre de usuario")
        # Si estoy actualizando, el nuevo username es diferente al de la instancia (esta cambiando
        # el username y existen usuarios registrados con el nuevo username)
        elif self.instance.username != data and len(user) != 0:
            raise serializers.ValidationError("Ya existe un usuario con ese nombre de usuario")
        else:
            return data
