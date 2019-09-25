import math

from rest_framework import serializers


class DataCenterSerializer(serializers.Serializer):
    name = serializers.CharField(required=True)
    servers = serializers.IntegerField(required=True, min_value=0, max_value=10**16)


class DevopsCapacitySerializer(serializers.Serializer):
    DM_capacity = serializers.IntegerField(required=True, min_value=1)
    DE_capacity = serializers.IntegerField(required=True, min_value=1)
    data_centers = serializers.ListField(child=DataCenterSerializer(), allow_empty=False)

    def validate(self, attrs):
        cities = [center['name'] for center in attrs['data_centers']]
        if len(cities) != len(set(cities)):
            raise serializers.ValidationError('Data center cities names must be unique.')
        return attrs

    def calculate_load(self):
        de_capacity = self.validated_data['DE_capacity']
        dm_capacity = self.validated_data['DM_capacity']
        de_required = 0
        dm_locations = {}
        for center in self.validated_data['data_centers']:
            servers_number = center['servers']
            de_required_without_dm = math.ceil(servers_number / de_capacity)
            de_required += de_required_without_dm
            if servers_number > dm_capacity:
                de_required_with_dm = math.ceil((servers_number - dm_capacity) / de_capacity)
            else:
                de_required_with_dm = 0
            dm_locations[center['name']] = de_required_without_dm - de_required_with_dm
        dm_best_location = max(dm_locations, key=dm_locations.get)
        minimum_de_required = de_required - dm_locations[dm_best_location]
        return {'DE': minimum_de_required, 'DM_data_center': dm_best_location}
