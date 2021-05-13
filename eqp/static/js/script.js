var audio = new Audio();
audio.src = "/static/audio/aquarela.mp3"; /* partir de onde está o html */
audio.currentTime = 14;
intervalo_captura = 3000;

var sol_amarelo_element = document.getElementById("sol-amarelo");
var socket = io.connect('http://' + document.domain + ':' + location.port);

window.onload = function()
{    
    Webcam.set({
        width: 1280,
        height: 720,
        image_format: "jpeg",
        jpeg_quality: 30
    });
    Webcam.attach("#minha-camera");
}

socket.on('connect', function ()
{ 
    setTimeout(capturarFoto, intervalo_captura);    
})

socket.on('valor-amarelo', function (valor)
{
    console.log('Recebendo valor amarelo: ', valor);
    sol_amarelo_element.removeAttribute("class");
    if (valor == 0)
    {
        sol_amarelo_element.classList.add('zero');
    }
    if (valor == 1)
    {
        sol_amarelo_element.classList.add('um');
    }
    else if (valor == 2)
    {
        sol_amarelo_element.classList.add('dois');
    }
    else if (valor >= 3)
    {
        sol_amarelo_element.classList.add('tres');
        audio.play();
    }
})

function capturarFoto()
{
    $("#minha-camera").css("border", "40px solid black");
    Webcam.snap( function(data_uri)
    {       
        Webcam.upload( data_uri, '/upload', function(code, text)
        {
            console.log('Envio da webcam');
            setTimeout(finalizarCaptura, 300);
        } );        
    } );
}

function finalizarCaptura()
{
    $("#minha-camera").css("border", "40px solid #CCCCCC");
    setTimeout(capturarFoto, intervalo_captura);
}