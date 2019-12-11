import os
import subprocess
from common import helper, settings

from IPython.core.magic import Magics, cell_magic, magics_class
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring

os.environ["JAVA_HOME"] = settings.JAVA_HOME
os.environ["SPARK_HOME"] = settings.SPARK_HOME


# project_name = 'my_project'
# project_version='1.0'
# scala_version = '2.11.12'
# settings.scala_version_red = scala_version[:-3]



@magics_class
class ScalaSparkLocal(Magics):

    def __init__(self, shell):
        super(ScalaSparkLocal, self).__init__(shell)
        self.argparser = helper.get_argparser()
        current_dir = os.getcwd()

        # dir paths and sbt file content
        self.src_dir = os.path.join(settings.root, settings.project_name,'src/main/scala')
        self.sbt_dir = os.path.join(settings.root, settings.project_name)
        self.sbt_content = 'name:=\"{}\"\nversion:=\"{}\"\nscalaVersion:=\"{}\"'\
                            .format(settings.project_name, settings.project_version, settings.scala_version)
        self.out_jar = os.path.join(settings.root, settings.project_name,\
                        'target/scala-{}/{}_{}-{}.jar'\
                        .format(settings.scala_version_red, settings.project_name, settings.scala_version_red, settings.project_version))

        # create src dir for the project
        if not os.path.exists(self.src_dir):
            os.makedirs(self.src_dir, exist_ok=False)
            print('created src project directory at {}'.format(self.src_dir))
        else:
            print('src project directory {} already exists'.format(self.src_dir))


    def compile(self):
        make_compile = 'sbt package'
        helper.popen(make_compile,
                     cwd=os.path.join(settings.root, settings.project_name))
        check_jar=os.path.exists(self.out_jar)
        i=0
        while(not check_jar or i>=10):
            print("{}-th attempt to compile...".format(i))
            helper.popen(make_compile,
                         cwd=os.path.join(settings.root, settings.project_name))
            check_jar=os.path.exists(self.out_jar)
            i+=1

    def run(self):
        spark_submit = os.path.join(settings.SPARK_HOME.replace(' ', '\ '), 'bin/spark-submit')
        master = 'local'

        print('Launching spark session...\n')

        make_run = ' '.join([spark_submit, ' --master ', master, self.out_jar ])
        helper.popen(make_run,
                    cwd=os.path.join(settings.root, settings.project_name) )


    @cell_magic
    def spark_compile(self, line='', cell=None):
        src_path = os.path.join(self.src_dir,
                   ''.join([settings.project_name,".scala"]))
        with open(src_path, "w") as f:
            f.write(cell)

        sbt_path = os.path.join(self.sbt_dir, settings.project_name+".sbt")
        with open(sbt_path, "w") as f:
            f.write(self.sbt_content)

        self.compile()

        #return line, cell


    @cell_magic
    def spark_run(self, line='', cell=None):
        self.spark_compile(line, cell)

        self.run()

        #return line, cell
