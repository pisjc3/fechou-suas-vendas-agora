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
      var im = new Inputmask('99.999.999/9999-99');
      im.mask(cnpjInput);
  }
}
