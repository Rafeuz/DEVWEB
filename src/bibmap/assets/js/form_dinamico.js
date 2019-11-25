$(document).ready(function() {
	var max_fields = 10; //Define o máximo de inputs gerados dinamicamente
	var wrapper = $(".input_fields_wrap");
	var add_button = $(".add_field_button");
	var numero_do_autor = 2; //Variavel que auxilia na alteração do atributo name da tag input, já começa em 2 por que o 1 já é cadastrado por padrão
	
	var quantidade_de_inputs = 1; //Contador inicial
	$(add_button).click(function(e){ //Função para adicionar inputs
		e.preventDefault();
		if(quantidade_de_inputs < max_fields){ //Verifica se a quantidade de inputs já atingiu o limite determinado
			quantidade_de_inputs++; //Incrementa o contador de inputs
			$(wrapper).append('<div class="form-group"><label for="nome">Autor:</label><select class="form-control" name="autor_nome' + numero_do_autor + '" id="autor_nome' + numero_do_autor + '">{%for autor in autores%}<option value="{{autor.id}}">{{autor.autor_nome}}</option>{%endfor%}</select><a href="#" class="remove_field">X</a></div>'); //Adiciona um input
			numero_do_autor++; //Incrementa para que o proximo input tenha um name diferente
		}
	});
	
	$(wrapper).on("click",".remove_field", function(e){ //Função para remover inputs
		e.preventDefault(); $(this).parent('div').remove(); quantidade_de_inputs--;
	})
});