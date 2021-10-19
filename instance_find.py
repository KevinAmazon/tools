import boto3
import sys

if len(sys.argv) < 2:
    print("USAGE: python3 %s c5. c4. c3. ..."%sys.argv[0])
    sys.exit(1)

instance_types = sys.argv[1:]

instance_type_filters = [a+"*" for a in instance_types]

ec2 = boto3.client('ec2')
region_names = [a['RegionName'] for a in ec2.describe_regions(AllRegions=True)['Regions']]
for name in region_names:
    print("Checking Region %s"%name)
    try:
        regional_client = boto3.client('ec2', region_name = name)
        for instance_type_filter in instance_type_filters:
            response = regional_client.describe_instance_type_offerings(LocationType='region',Filters=[{'Name': 'instance-type', 'Values':[instance_type_filter]}])
            #print([entry['InstanceType'] for entry in response['InstanceTypeOfferings']])
            print("\t%s instance type count = %i"%(instance_type_filter,len(response['InstanceTypeOfferings'])))
    except Exception as err:
        #print(err)
        print("\tNo API Access to this region.")
