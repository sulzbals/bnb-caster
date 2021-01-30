class Actor():
  def __init__(self, value, idx):
    self.value = value  # Valor (custo) do ator
    self.idx = idx      # Índice do ator

    self.groups = set() # Conjunto dos grupos representados pelo ator

  def addGroup(self, group):
    '''
    Adiciona grupo ao conjunto de grupos representados
    '''
    self.groups.add(group)