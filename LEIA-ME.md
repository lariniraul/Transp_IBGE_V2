# Consulta Municipal • SP

Aplicação Python local com interface no navegador. Consulta receitas e despesas da API pública do TCE-SP, por cidade e intervalo de meses, e indicadores municipais do IBGE. Não exige chave de API. Requer Python 3.10 ou superior e internet.

## Iniciar

Abra um terminal nesta pasta e execute:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

O Streamlit abre o navegador. Se não abrir automaticamente, acesse http://localhost:8501. Para encerrar, pressione Ctrl+C no terminal.

## Usar

1. Escolha Receitas ou Despesas no menu lateral.
2. Escolha a cidade; o padrão é Cosmópolis/SP.
3. Informe início e fim em MM/AAAA; o padrão é janeiro de 2026.
4. Clique em Consultar. As tabelas e resumos aparecem na tela, sem download.
5. Veja o resumo de todos os meses. Use Mês dos detalhes para acessar um mês diretamente.
6. Filtre por órgão e fonte ou movimentação, busque texto e navegue entre páginas. Por padrão, a tabela inclui todos os registros; escolha 25, 50 ou 100 linhas para paginar.

A exportação CSV é opcional e inclui todos os registros filtrados, não apenas a página visível. Valores e identificadores originais são preservados no CSV. O intervalo pode atravessar anos, com limite de 60 meses por consulta.

## Cobertura e interpretação

### Indicadores do IBGE

No menu lateral, escolha **Indicadores do IBGE**. Selecione um município de São Paulo, o conjunto de indicadores e um ou mais anos disponíveis; clique em **Consultar IBGE**. O padrão é Cosmópolis e o último ano da tabela escolhida.

- População residente, área e densidade: Censo 2022, tabela SIDRA 4714. Não são estimativas atuais de população.
- PIB municipal a preços correntes: tabela SIDRA 5938, variável 37. A unidade retornada é Mil Reais e é exibida sem alterar a escala.
- Os anos disponíveis são obtidos diretamente do IBGE. O período mensal de receitas e despesas não se aplica a esses indicadores.
- A tabela preserva sinais especiais da fonte; eles não são convertidos para zero.
- Dados reais do Censo 2022 e do PIB de 2022/2023 de Cosmópolis foram testados nesta atualização.
- Fontes: https://servicodados.ibge.gov.br/api/docs/localidades e https://sidra.ibge.gov.br/tabela/4714 e https://sidra.ibge.gov.br/tabela/5938.

### Receitas e despesas

- Fonte: https://transparencia.tce.sp.gov.br/apis
- Atende municípios jurisdicionados ao TCE-SP; não é uma consulta nacional nem uma conexão direta ao sistema da prefeitura.
- Receitas: todas as fontes e órgãos disponíveis na resposta, antes dos filtros de tela.
- Despesas: valores agrupados pela movimentação original da API. Empenhos, liquidações, pagamentos, reforços e anulações não são somados em um total único e não são tratados como saldo líquido.
- O painel informa falhas e meses sem registros. Resultado vazio não comprova arrecadação ou despesa zero. Um retorno com registros também não comprova completude contábil.
- A documentação publicada ainda menciona exercícios antigos. Receitas de Cosmópolis de janeiro a março de 2026 foram verificadas na API durante esta atualização (170, 172 e 178 registros, respectivamente). Outros municípios e períodos dependem da disponibilidade do serviço.
- Valores inválidos geram falha no respectivo mês, em vez de serem convertidos silenciosamente para zero.
- A tabela de detalhes exibe moeda como texto; sua ordenação por valor na interface é textual.

## Arquivos

- app.py: interface Streamlit.
- api.py: consultas HTTP, validação do período e valores.
- ibge.py: cliente das APIs de localidades e indicadores do IBGE.
- painel_ibge.py: interface de seleção e visualização dos indicadores.
- requirements.txt: dependências.

## Atualizar no GitHub

Envie novamente app.py e LEIA-ME.md e adicione ibge.py e painel_ibge.py na mesma pasta de app.py. Mantenha api.py e requirements.txt. Não envie __pycache__, work ou arquivos de teste. Se já publicou no Streamlit Community Cloud, salve as alterações na mesma branch usada pela implantação.

Nenhum dado fictício é apresentado como resultado. A aplicação consulta os meses sequencialmente e mantém resultados parciais com aviso se o serviço falhar.
