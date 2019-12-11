jdk_version='8'
scala_version = '2.11.12'
scala_version_red = scala_version[:-3]
spark_version='2.4.4'
hadoop_version='2.7'
root='/content'
spark_dest='/content/gdrive/My Drive/opt'
JAVA_HOME= "/usr/lib/jvm/java-{}-openjdk-amd64".format(jdk_version)
SPARK_HOME= '{}/spark-{}-bin-hadoop{}'\
            .format(spark_dest, spark_version, hadoop_version)


project_name = 'my_project'
project_version='1.0'
