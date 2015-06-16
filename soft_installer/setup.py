
class LinuxSoft:
    command_install = ""

    def install(self, softName):
        if isinstance(softName,str):
            softName = (softName, )
        import os
        for i in softName:
            os.system(self.command_install % i)
        pass

    def uninstall(sewlf, softName):
        pass

class Ubuntu(LinuxSoft):
    command_install = "apt-get install -y %s"
    pass

softs = (
    'ctags', 'git','svn','nginx'
)

curOS = Ubuntu()
curOS.install(softs)
