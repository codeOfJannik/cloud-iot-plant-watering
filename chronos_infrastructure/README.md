# Terrafrom - Chronos AWS Infrastructure 
The _chronos_infrastructure_ directory contains terraform scripts, which declare the instructions how the AWS Components
are set up. This scripts are be split up in three modules:
- [IoT Events](iot_events/README.md)
- [IoT Core](iot_core/README.md)
- [Docker](docker/README.md)

To get more information, see the corresponding module README's

The [_main.tf_](./main.tf) in the _chronos_infrastructure_ directory contains the AWS profile and region name and run 
the three different modules.
The profile needs to be declared in the _.aws/credentials_ file with the following specifications:

```
[chronos]                                   # your profile name
aws_access_key_id = your access key         # required
aws_secret_access_key = your secret key     # required
region = us-east-1                          # optional
```

The profile name need to be the same as the declared profile name in the [_main.tf_](./main.tf) file.
A region is required either in the AWS credential file or in the _main.tf_ file. If in both files a region is specified,
this will be used, which is in the _main.tf_ file.

To set dependencies between the different modules, for each module a ```*_dependencies``` output variable is declared,
containing a list of resources, which need to be set as dependency in an other module. The '*' stands for the module,
for which the dependencies it will be used for. To see what dependencies are set, see the _outputs.tf_ files in the 
different modules.

The dependencies list is passed in the root _main.tf_ file to the corresponding modules, which can read in the list with 
a variable template _dependencies_, also a list.
This dependencies are important to tell terraform to wait for other resources.