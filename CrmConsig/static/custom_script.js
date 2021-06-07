$('.main-search.morphsearch-search .input-group input.form-control').keyup(function(){
    var typed_value = $(this).val();
    $('#id_cpf_search').val(typed_value);
    $('#id_matricula_search').val(typed_value);
});