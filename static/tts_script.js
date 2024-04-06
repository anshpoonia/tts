let num_voice = {"male": 0, "female": 0};
let button = document.querySelector(".button");
let input_tag = document.querySelector(".input");
let gender_tag = document.querySelector(".gender");
let voice_tag = document.querySelector(".voice");
let lang_tag = document.querySelector(".lang");
let audio_tag = document.querySelector(".audio")
let voice_holder = document.querySelector(".voice_holder")


button.addEventListener("click", () => {
    let text = input_tag.value;
    let gender = gender_tag.value;
    let voice = voice_tag.value;
    let lang = lang_tag.value;

    if (text.length > 0)
    {
        disable_input()
        console.log(text, gender, voice, lang)
        if (gender === "custom" && voice.length !== 4)
        {
            audio_tag.innerHTML = "Invalid Voice Code"
            enable_input();
        }
        else {
            send(text, gender, voice, lang);
        }
    }
    else {
        input_tag.focus()
    }
});


gender_tag.addEventListener("change", () => {
    if (gender_tag.value === "custom")
    {
        voice_holder.innerHTML = `<input type="text" maxlength="4" minlength="4" name="voice" class="voice">`
        audio_tag.innerHTML = `Add your sample <a href="/sample"> here.</a>`
        voice_tag = document.querySelector(".voice");
    }
    else {
        voice_holder.innerHTML = `<select name="voice" class="voice"></select>`
        voice_tag = document.querySelector(".voice");
        add_voices(gender_tag.value);
    }
});

document.addEventListener("DOMContentLoaded", () => {
    get_voices();
    input_tag.focus();
});


function send(text, gender, voice, lang)
{
    audio_tag.innerHTML = "";
    let url = "/speak?text="+text+"&tag="+gender+"&speaker="+voice.toString()+"&lang="+lang;

    fetch(url)
        .then(res => {
            console.log(res.ok, res.status)
            if (!res.ok){
                return res.json().then(error => {
                    throw new Error(error["error"]);
                });
            }

            console.log("blob");
            return res.blob();
        })
        .then(file => {
            let audio = document.createElement("audio");
            audio.src = URL.createObjectURL(file);
            audio.controls = true;
            audio.autoplay = true;
            audio_tag.appendChild(audio);
            enable_input();
        })
        .catch(error => {
            handle_error(error.message)
        });
}

function disable_input()
{
    gender_tag.disabled = true;
    input_tag.disabled = true;
    voice_tag.disabled = true;
    lang_tag.disabled = true;
    button.disabled = true;
}

function enable_input()
{
    gender_tag.disabled = false;
    input_tag.disabled = false;
    voice_tag.disabled = false;
    lang_tag.disabled = false;
    button.disabled = false;
}

function handle_error(message){
    audio_tag.innerHTML = message
    enable_input();
}

function get_voices()
{
    fetch("/speakers")
        .then(res => res.json())
        .then(data => {
            num_voice = data
            voice_holder.innerHTML = `<select name="voice" class="voice"></select>`
            voice_tag = document.querySelector(".voice");
            add_voices("male");
        });
}

function add_voices(gender)
{
    let n = parseInt(num_voice[gender]);
    for (let i = 0; i < n ; i++)
    {
        let option = document.createElement("option");
        option.value = (i+1).toString();
        option.innerText = "v"+(i+1);
        voice_tag.appendChild(option)
    }
}