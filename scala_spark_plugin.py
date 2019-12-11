from v0.v0 import ScalaSparkLocal as ScalaSpark
from common import helper, settings

# from google.colab import drive
#
#
# class Colab_Mounter:
#     def __init__(self, mounting_point='/content/gdrive'):
#         self.mounting_point=mounting_point
#
#     def mount(self):
#         drive.mount(self.mounting_point)

class Linux_Pkg_Installer:

    @staticmethod
    def install_jdk():
        helper.popen('apt-get install openjdk-{}-jdk-headless -qq 1> /dev/null'\
                     .format(settings.jdk_version))

    @staticmethod
    def install_scala():
        helper.popen('apt-get install scala')

    @staticmethod
    def install_spark():
        mkdir = 'mkdir -p {}'\
                .format(settings.spark_dest.replace(' ','\ '))
        curl = 'curl -LJO "https://www-us.apache.org/dist/spark/spark-{}/spark-{}-bin-hadoop{}.tgz"'\
                .format(settings.spark_version,
                        settings.spark_version,
                        settings.hadoop_version)
        tar = 'tar xvf spark-{}-bin-hadoop{}.tgz'\
              .format(settings.spark_version,settings.hadoop_version)
        helper.popen(mkdir, cwd=settings.root)
        helper.popen(' && '.join([curl, tar]), cwd=settings.spark_dest)

    @staticmethod
    def install_sbt():
        echo = ' echo "deb https://dl.bintray.com/sbt/debian /" '
        tee =  ' sudo tee -a /etc/apt/sources.list.d/sbt.list '
        sbt_list = ' | '.join( [echo, tee] )
        curl = ' curl -sL "https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x2EE0EA64E40A89B84B2DF73499E82A75642AC823" | sudo apt-key add  '
        update = 'sudo apt-get update'
        sbt = 'sudo apt-get install sbt'
        # which = 'which sbt'
        helper.popen(' && '.join([sbt_list, curl, update, sbt]) )


# LOAD EXTENSION FUNCTION
def load_ipython_extension(ip):
    # mount gdrive at '/content/gdrive' --> must be done from outside if package has been installed locally. Can be left here when pkg will be curlable from www
    # mounter = Colab_Mounter()
    # mounter.mount()

    # install linux packages
    apt_get = Linux_Pkg_Installer()
    apt_get.install_jdk()
    apt_get.install_scala()
    apt_get.install_spark()
    apt_get.install_sbt()


    scala_spark_plugin = ScalaSpark(ip)
    ip.register_magics(scala_spark_plugin)
