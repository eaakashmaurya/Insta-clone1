$('select').on('change', function (e) {
    var optionSelected = $("option:selected", this);
    var valueSelected = this.value;
    console.log(typeof valueSelected, valueSelected);
    var t_input = document.getElementById("textbox");
    if (valueSelected == 'sans')
    {
        console.log("Cool!");
        enableTransliteration(t_input, "sa");

    }
    else
    {
        disableTransliteration(t_input);
    }
});