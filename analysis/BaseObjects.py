import numpy as np
from collections import namedtuple
import csv

Cell_ = namedtuple('Cell', 'x y z genotype')
Cell_.__new__.__defaults__ = ( 0, 0, 0, -1 )

class Cell(Cell_):
  """
	Generic holder for cell details.
	@params:
	  id = cell ID
	  x,y,z = coordinates of the cell in the tumor
	  genotype = the genotype ID of this cell
  """
  @staticmethod
  def load_cells(file_name):
	"""
	Returns a list of Cells
	@params:
	  file_name
	"""
	cells = []
	with open( file_name, 'r' ) as cell_file:
	  for row in csv.reader(cell_file):
		cells.append( Cell( *map( int, row[0].split(' ' ) ) ) )
	return cells

Genotype_ = namedtuple('Genotype', 'original_id parent_genotype n_resistant n_driver frequency snps')
Genotype_.__new__.__defaults__ = (-1, -1, 0, 0, 1, [])

class Genotype(Genotype_):
  """
	Generic holder for Genotypes
	@params
	  orignal_id = the original ID of this genome during the simulation
	  parent_genotype = the parent_ID of this genome
	  n_resistant = number of resistant mutations
	  n_driver = number of driver mutations
	  frequency = the number of cells with this genotype
	  snps = the sequence of SNPs in this genotype.
  """
  @staticmethod
  def load_genotypes(file_name):
	"""
	Returns a list of genotypes
	@params:
	  file_name
	"""
	genotypes = []
	with open( file_name, 'r' ) as genotype_file:
	  for row in csv.reader( genotype_file ):
		details, sequence = row[0].split('\t') # split on the tab
		original_id, parent_genotype, numbers, frequency = details.split('  ')
		n_resistant, n_driver = numbers.split(' ')
		sequence = filter( lambda SNP: len(SNP), sequence.split(' ') ) # remove blank SNPs
		sequence = map( int , sequence ) # convert everything into ints
		genotypes.append( Genotype( int(original_id), int(parent_genotype), int(n_resistant), \
					   int(n_driver), int(frequency), sequence ) )
	return genotypes

class Tumor(object):
	def __init__( self, cells, genotypes ):
		"""
			Generic tumor object containing cells and genotypes.
			@params:
				cells: a list of cells
				genotypes: a list of genotypes
		"""
		self.cells = cells
		self.genotypes = genotypes
		self.number_of_cells = len(cells)
		self.number_of_genotypes = len(genotypes)
	@staticmethod
	def from_files( cell_file, genome_file ):
		"""
			Returns a tumor from cell and genotype data files
			@params:
				cell_file : file containing cell positions and genotypes
				genome_file : file containing genome data
		"""
		return Tumor( Cell.load_cells( cell_file ), \
					 Genotype.load_genotypes( genome_file ) )
