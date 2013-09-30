__all__ = ['SU2_Plugin']

import os, sys, shutil, copy
import subprocess

from openmdao.main.api import Component, Variable
from openmdao.lib.datatypes.api import Instance

from SU2.io.config import Config
from SU2.run.interface import build_command, run_command

# ------------------------------------------------------------
#  Setup
# ------------------------------------------------------------

SU2_RUN = os.environ['SU2_RUN'] 
sys.path.append( SU2_RUN )

# SU2 suite run command template
base_Command = os.path.join(SU2_RUN,'%s')

# check for slurm
slurm_job = os.environ.has_key('SLURM_JOBID')
    
# set mpi command
if slurm_job:
    mpi_Command = 'srun -n %i %s'
else:
    mpi_Command = 'mpirun -np %i %s'


class ConfigVar(Variable):
    def __init__(self, default_value=None, iotype=None, desc=None, 
                 **metadata):
        super(ConfigVar, self).__init__(default_value=default_value,
                                    	**metadata)

    def validate(self, obj, name, value):
        """ Validates that a specified value is valid for this trait.
        Units are converted as needed.
        """
        if not isinstance(value, Config):
        	raise TypeError("value of '%s' must be a Config object" % name)
        return value

# ------------------------------------------------------------
#  SU2 Suite Interface Functions
# ------------------------------------------------------------

class DDC(Component):
    """ run SU2_DDC 
        partitions set by config.NUMBER_PART
        currently forced to run serially
    """

    config = ConfigVar(Config(), iotype='in')

    def execute(self):
	    # local copy
	    konfig = copy.deepcopy(config)
	    
	    tempname = 'config_DDC.cfg'
	    konfig.dump(tempname)
	  
	    processes = konfig['NUMBER_PART']
	    
	    the_Command = 'SU2_DDC ' + tempname
	    the_Command = build_command( the_Command , processes )
	    run_command( the_Command )
	    
	    #os.remove(tempname)


# def CFD(config):
#     """ run SU2_CFD
#         partitions set by config.NUMBER_PART
#     """
    
#     konfig = copy.deepcopy(config)
    
#     tempname = 'config_CFD.cfg'
#     konfig.dump(tempname)
    
#     processes = konfig['NUMBER_PART']
    
#     the_Command = 'SU2_CFD ' + tempname
#     the_Command = build_command( the_Command , processes )
#     run_command( the_Command )
    
#     #os.remove(tempname)
    
#     return

# def MAC(config):
#     """ run SU2_MAC
#         partitions set by config.NUMBER_PART
#         currently forced to run serially
#     """    
#     konfig = copy.deepcopy(config)
    
#     tempname = 'config_MAC.cfg'
#     konfig.dump(tempname)
    
#     # must run with rank 1
#     processes = konfig['NUMBER_PART']
#     processes = min([1,processes])    
    
#     the_Command = 'SU2_MAC ' + tempname
#     the_Command = build_command( the_Command , processes )
#     run_command( the_Command )
    
#     #os.remove(tempname)
    
#     return

# def MDC(config):
#     """ run SU2_MDC
#         partitions set by config.NUMBER_PART
#         forced to run in serial, expects merged mesh input
#     """
#     konfig = copy.deepcopy(config)
    
#     tempname = 'config_MDC.cfg'
#     konfig.dump(tempname) 
    
#     # must run with rank 1
#     processes = konfig['NUMBER_PART']
    
#     the_Command = 'SU2_MDC ' + tempname
#     the_Command = build_command( the_Command , processes )
#     run_command( the_Command )
    
#     #os.remove(tempname)
    
#     return

# def GPC(config):
#     """ run SU2_GPC
#         partitions set by config.NUMBER_PART
#     """    
#     konfig = copy.deepcopy(config)
    
#     tempname = 'config_GPC.cfg'
#     konfig.dump(tempname)   
    
#     processes = konfig['NUMBER_PART']
    
#     the_Command = 'SU2_GPC ' + tempname
#     the_Command = build_command( the_Command , processes )
#     run_command( the_Command )
    
#     #os.remove(tempname)
    
#     return

# def GDC(config):
#     """ run SU2_GDC
#         partitions set by config.NUMBER_PART
#         forced to run in serial
#     """    
#     konfig = copy.deepcopy(config)
    
#     tempname = 'config_GDC.cfg'
#     konfig.dump(tempname)   
    
#     # must run with rank 1
#     processes = konfig['NUMBER_PART']
        
#     the_Command = 'SU2_GDC ' + tempname
#     the_Command = build_command( the_Command , processes )
#     run_command( the_Command )
    
#     #os.remove(tempname)
    
#     return

# def SMC(config):
#     """ run SU2_SMC
#         partitions set by config.NUMBER_PART
#     """    
#     konfig = copy.deepcopy(config)    
    
#     tempname = 'config_SMC.cfg'
#     konfig.dump(tempname)   
    
#     # must run with rank 1
#     processes = konfig['NUMBER_PART']
#     processes = min([1,processes])       
    
#     the_Command = 'SU2_SMC ' + tempname
#     the_Command = build_command( the_Command , processes )
#     run_command( the_Command )
    
#     #os.remove(tempname)
    
#     return

# def PBC(config):
#     """ run SU2_PBC
#         partitions set by config.NUMBER_PART
#         currently forced to run serially
#     """    
#     konfig = copy.deepcopy(config)
    
#     tempname = 'config_PBC.cfg'
#     konfig.dump(tempname)
    
#     # must run with rank 1
#     processes = konfig['NUMBER_PART']
#     processes = min([1,processes])      
    
#     the_Command = 'SU2_PBC ' + tempname
#     the_Command = build_command( the_Command , processes )
#     run_command( the_Command )
    
#     #os.remove(tempname)
    
#     return
        
# def SOL(config):
#     """ run SU2_SOL
#       partitions set by config.NUMBER_PART
#     """
  
#     konfig = copy.deepcopy(config)
    
#     tempname = 'config_SOL.cfg'
#     konfig.dump(tempname)
  
#     # must run with rank 1
#     processes = konfig['NUMBER_PART']
    
#     the_Command = 'SU2_SOL ' + tempname
#     the_Command = build_command( the_Command , processes )
#     run_command( the_Command )
    
#     #os.remove(tempname)
    
#     return

      
