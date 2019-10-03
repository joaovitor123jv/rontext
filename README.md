# Lista de tarefas a serem implementadas

### Correções implementadas:
* Tipo de acesso, alterado de IN\_ACCESS para IN\_OPEN, identificando somente
aberturas de arquivos

* Implementei um método de checagem para o caminho do arquivo, para que o
  usuário possa configurar o que deve ser removido dos seus resultados, já que
  cada usuário pode ter um perfil de uso diferente, e o usuário comum nem
  conhece git ou IDE. É possível que o tempo de inserção possa ser alterado por
  isso, vou realizar um teste de inserção novamente e comparar com os
  resultados dos testes já obtidos só por precaução.


### O que ainda preciso fazer:
1. Verificar a possibilidade de ter as pastas:
    * uma por evento
    * uma por localização
2. Pensar na validação do sistema
    * Validação e verificação de software
    * Teste caixa preta

3. Experimentar 

4. Escrever o que falta da monografia

5. Escrever e entregar para revisão

6. Fazer os slides
    * Escrever o que falta (uma lista do que preciso escrever ainda)


### Problemas identificados:
* Durante a leitura de qualquer arquivo .mp3, o evento "OPEN", é identificado várias
vezes, dependendo do player de música
    * Lembrar de colocar como "ameaça à funcionalidade", deixar como trabalho futuro

* Quando "ouvindo" recursivamente a partir de um diretório, todos os arquivos
  podem disparar eventos, incluindo pacotes dentro de projetos node,
  `./node_modules/`, arquivos que são re-lidos várias vezes por um servidor
  (routes.rb, num servidor rails), alterações em diretórios `.git` e leituras
  realizadas por IDE's e editores de texto para melhorar o autocomplete.  

  Ao abrir dois projetos (um grande com `rails` e um pequeno com `react`) mais
  de dois mil arquivos começaram a ser acessados muito rapidamente. O
  `filesystem_listener` acabou sobrecarregado e algumas vezes ocorreu o erro de
  banco de dados bloqueado.  

  Durante o tempo de inserção desses milhares de arquivos, literalmente, o
  retorno do sistema foi muito lento, o dispositivo de armazenamento estava sobrecarregado.

