class Node():
  '''
  Nó de uma árvore B&B
  '''
  def __init__(self, idx, cost, candidates, cast, represented, num_roles):
    self.idx = idx                           # Índice do candidato
    self.cost = cost                         # Custo acumulado da árvore
    try:
      self.candidate = candidates[0]         # Candidato representado
      self.next_candidates = candidates[1:]  # Próximos candidatos na fila
    except IndexError:
      self.candidate = None                  # Candidato representado
      self.next_candidates = []              # Próximos candidatos na fila
    self.cast = cast                         # Candidatos elencados
    self.represented = represented           # Grupos representados
    self.num_roles = num_roles               # Número de vagas totais

  def branch(self):
    '''
    Função Branch (cria nós filhos)
    '''
    # Se o elenco até o momento é menor do que o número de vagas, novos
    # candidatos podem ser elencados (BRANCH IN):
    if len(self.cast) < self.num_roles:
      yield self.__class__(
        self.idx + 1,
        self.cost + self.candidate.value,
        self.next_candidates,
        self.cast + [self.candidate],
        self.represented | self.candidate.groups,
        self.num_roles
      )

    # Se o número de vagas não preenchidas é menor do que o número de candidatos
    # restantes, novos candidatos podem ser rejeitados (BRANCH OUT):
    if self.num_roles - len(self.cast) < len(self.next_candidates) + 1:
      yield self.__class__(
        self.idx + 1,
        self.cost,
        self.next_candidates,
        self.cast,
        self.represented,
        self.num_roles
      )


class LazyNode(Node):
  '''
  Nó de uma árvore B&B utilizando Lazy Bound
  '''
  def bound(self):
    '''
    Função Bound (Define o potencial de encontrar uma solução melhor na
    subárvore)
    '''
    # Retorna o custo acumulado na raiz da subárvore:
    return self.cost


class GreedyNode(Node):
  '''
  Nó de uma árvore B&B utilizando Greedy Bound
  '''
  def bound(self):
    '''
    Função Bound (Define o potencial de encontrar uma solução melhor na
    subárvore)
    '''
    # Simula o elenco menos custoso possível:
    sim_cast = self.next_candidates[:self.num_roles-len(self.cast)]

    # Retorna o menor custo possível da subárvore:
    return self.cost + sum(candidate.value for candidate in sim_cast)


class NodeFactory():
  '''
  Fábrica de nós (instancia pela função bound selecionada)
  '''
  def __init__(self, bound):
    if bound == "Lazy Bound":
      self.Node = LazyNode
    else:
      self.Node = GreedyNode


class Tree():
  '''
  Árvore B&B
  '''
  def __init__(self, candidates, num_roles):
    self.candidates = candidates  # Candidatos
    self.num_roles = num_roles    # Número de vagas

    # Estrutura de pilha (lista) para simular a árvore:
    self.stack = [
    ]

  def push(self, node):
    '''
    Empilha nó à pilha que simula a árvore
    '''
    self.stack.insert(0, node)

  def pop(self):
    '''
    Desempilha nó da pilha que simula a árvore
    '''
    return self.stack.pop(0)

  def isEmpty(self):
    '''
    Checa se a pilha está vazia
    '''
    return not self.stack


class CastingProblem():
  '''
  Problema do Elenco Representativo
  '''
  def __init__(self, candidates, groups, num_roles, bound):
    self.candidates = candidates  # Candidatos
    self.groups = groups          # Grupos
    self.num_roles = num_roles    # Número de vagas

    # Instancia fábrica de nós de acordo com a função bound escolhida:
    self.factory = NodeFactory(bound)

    # Custo mínimo (ótimo) inicializado com valor não plausível:
    self.min_cost = sum([candidate.value for candidate in self.candidates]) + 1

    # Ordena os candidatos por valor (custo):
    self.candidates.sort(key=lambda candidate: candidate.value)

    # Lista de candidatos elencados:
    self.cast = []

    # Árvore a ser construída:
    self.tree = Tree(self.candidates, self.num_roles)

  def solve(self):
    '''
    Resolve o problema
    '''
    # Nó raiz:
    self.tree.push(
      self.factory.Node(
        0,
        0,
        self.candidates,
        [],
        set(),
        self.num_roles
      )
    )

    while not self.tree.isEmpty():
      # Percorre o próximo nó:
      node = self.tree.pop()

      # Se é um nó folha, pode ser uma solução:
      if node.idx >= len(self.candidates):
        # Se todas as vagas foram preenchidas e todos os grupos foram
        # representados, é uma solução plausível:
        if len(node.cast) == self.num_roles and node.represented == self.groups:
          # Se a solução (custo) atual é melhor que a solução ótima até então,
          # esta é a nova solução ótima:
          if node.cost < self.min_cost:
            self.cast = node.cast
            self.min_cost = node.cost
      else:
        # Obtém valor da função bound:
        bound = node.bound()

        # Se a subárvore a ser construída tem potencial de resultar em uma
        # solução melhor:
        if bound < self.min_cost:
          for branched_node in list(node.branch()):
            self.tree.push(branched_node)

    return self.cast, self.min_cost