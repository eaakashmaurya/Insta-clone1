let t_input = document.getElementsByClassName("transliterate_input_sn");

var i;
for (i = 0; i < t_input.length; i++) {
    console.log("hassh!");
    enableTransliteration(t_input[i], "sa");
}