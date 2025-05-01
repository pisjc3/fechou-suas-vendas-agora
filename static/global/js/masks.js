function phoneMask(inputId) {
  var telefoneInput = document.getElementById(inputId);
  if (telefoneInput) {
    var im = new Inputmask("(99) 9999-9999", {
      mask: ["(99) 99999-9999"],
    });
    im.mask(telefoneInput);
  }
}

function cnpjMask(inputId) {
  var cnpjInput = document.getElementById(inputId);
  if (cnpjInput) {
    var im = new Inputmask("99.999.999/9999-99");
    im.mask(cnpjInput);
  }
}

function currencyMask(value) {
  const numberValue = typeof value === "string" ? parseFloat(value) : value;
  if (isNaN(numberValue)) return "R$ 0,00";

  return numberValue.toLocaleString("pt-BR", {
    style: "currency",
    currency: "BRL",
  });
}
