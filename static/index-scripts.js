document.addEventListener("keypress", handleKeyPress);


function handleKeyPress(event) {
    if (event.keyCode === 13) {
        event.preventDefault()
        showresults(event);
    }
}

function scrollToPage(pageId) {
    var menu = document.getElementById("nav");
    var page = document.getElementById(pageId);
    page.scrollIntoView({ behavior: 'smooth' });
}

var activeButton = "searchquery";

function setHTMLContent(elementId, content) {
    document.getElementById(elementId).innerHTML = content;
}

function showresults(event) {
    event.preventDefault(); 

    var resultPage = document.getElementById("result-page");

    var query = document.getElementById("query");
    querytext = query.value

    var loading = "<div id='summary-loading' class='loading'><p class='load-text'>G</p></div>"

    if (resultPage.style.display === "none" && querytext === "") {
        console.log("True - null")
    }

    else {
        
        if (resultPage.style.display === "flex") {
            var query = document.getElementById("results-query");
            querytext = query.value
        }

        var original = document.getElementById("main-container");
        original.style.display = "none";

        var resultPage = document.getElementById("result-page");
        resultPage.style.display = "flex";

        var resultsquery = document.getElementById("results-query");
        resultsquery.innerText = querytext

        if (activeButton === "searchquery") {
            var summarizedTextDiv = document.getElementById('summarized-text');
            var originalTextDiv = document.getElementById('original-text'); 
            summarizedTextDiv.innerHTML = loading
            originalTextDiv.innerHTML = loading
            
            fetch('/showgoogleresults', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query: querytext})
            })
            .then(response => response.json())
            .then(summary => {
                var data = summary.data;
                
                var bunchorg = "<div class='parent' style='overflow-y:auto; overflow-x:wrap; display:flex; flex-direction: column; width:100%;'>";
                var originalTextContent = "";
                data.forEach(function(item) {
                    originalTextContent += "<div style='padding: 3%; overflow:wrap; border-radius:15px; margin:1%; background-color:black; color:white; width:92%'>";
                    originalTextContent += "<strong style='font-weight:lighter'>" + item[0] + ":</strong><br>";
                    originalTextContent += "<a href='" + item[1] + "' style='color: rgba(100, 35, 100, 0.9); text-decoration: none;'>" + item[1] + "</a>";
                    originalTextContent += "</div>";
                });
                bunchorg += originalTextContent;
                bunchorg += "</div>";

                setHTMLContent('original-text', bunchorg);
            })
            .catch(error => {
                console.error('Error:', error);
            });

            fetch('/querysummarize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ query : querytext })
            })
            .then(response => response.text())
            .then(summary => {
                summarizedTextDiv.innerText = summary;
            })
            .catch(error => {
                console.error('Error:', error);
            });

        } else if (activeButton === "ytvideo") {
            var videoUrl = querytext
            var summarizedTextDiv = document.getElementById('summarized-text'); 
            var originalTextDiv = document.getElementById('original-text'); 
            summarizedTextDiv.innerHTML = loading
            originalTextDiv.innerHTML = loading
            
            fetch('/videotranscript', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url: videoUrl })
            })
            .then(response => response.json())
            .then(results => {
                summarizedTextDiv.innerText = results.summarized_transcript;;
                originalTextDiv.innerText = results.transcript
            })
            .catch(error => {
                console.error('Error:', error);
            });

        } else {
            var websiteUrl = querytext
            var summarizedTextDiv = document.getElementById('summarized-text');
            var originalTextDiv = document.getElementById('original-text'); 
            summarizedTextDiv.innerHTML = loading
            originalTextDiv.innerHTML = loading
            
            fetch('/webpagesummarize', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ url: websiteUrl })
            })
            .then(response => response.text())
            .then(summary => {
                summarizedTextDiv.innerText = summary;
            })
            .catch(error => {
                console.error('Error:', error);
            });

            originalTextDiv.innerText = ""

            var iframe = document.createElement("iframe");
            iframe.src = websiteUrl;
            iframe.style.width = "100%";
            iframe.style.height = "100%";
            iframe.style.borderRadius = "15px";
            iframe.style.borderWidth = "0px";

            originalTextDiv.appendChild(iframe);
            
        }    
    }
}

function resultpagesearch(event){
    event.preventDefault(); 
}

function toggleActive(button, placeholder, resulthead, originalhead, id) {
    var buttons = document.getElementsByClassName("mb");
    for (var i = 0; i < buttons.length; i++) {
        buttons[i].classList.remove("active");
    }

    button.classList.add("active");
    document.getElementById("query").placeholder = placeholder;
    document.getElementById("results-query").placeholder = placeholder;
    document.getElementById("originalhead").innerText = originalhead;
    document.getElementById("resulthead").innerText = resulthead;
    document.getElementById("results-query").innerText = "";

    activeButton = id
}

function readText() {
    var textToRead = document.getElementById('summarized-text').innerText;
    responsiveVoice.speak(textToRead);
}