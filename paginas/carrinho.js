const lista = document.getElementById('itens');
const form = document.getElementById('venda');
function dinheiro(v) {
  return 'R$ ' + v.toLocaleString('pt-BR', {minimumFractionDigits: 2, maximumFractionDigits: 2});
}
function calcular() {
  let total = 0, unidades = 0;
  lista.querySelectorAll('.item-venda').forEach(linha => {
    const preco = Number(linha.querySelector('select').selectedOptions[0].dataset.preco || 0);
    const quantidade = Number(linha.querySelector('input').value) || 0;
    linha.querySelector('.sub').textContent = preco ? dinheiro(preco * quantidade) : '—';
    total += preco * quantidade;
    if (preco) unidades += quantidade;
  });
  document.getElementById('total').textContent = dinheiro(total);
  document.getElementById('unidades').textContent = unidades;
}
function adicionar() {
  lista.appendChild(document.getElementById('modelo').content.cloneNode(true));
  calcular();
}
document.getElementById('adicionar').onclick = adicionar;
form.addEventListener('input', calcular);
form.addEventListener('click', e => {
  const botao = e.target.closest('button');
  const linha = botao && botao.closest('.item-venda');
  if (!linha) return;
  if (botao.dataset.passo) {
    const campo = linha.querySelector('input');
    campo.value = Math.max(1, Number(campo.value) + Number(botao.dataset.passo));
  } else if (lista.children.length > 1) {
    linha.remove();
  }
  calcular();
});
adicionar();
