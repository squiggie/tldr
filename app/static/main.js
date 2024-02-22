$(document).ready( function () {

    // To ensure all AJAX calls have this in the header
    $.ajaxSetup({
        contentType: "application/json; charset=utf-8"
    });

    /* setInterval(updateArticles, 30000);

    async function updateArticles() {
        const container = document.querySelector('.columns.is-multiline');
        const articleCards = document.querySelectorAll('.card');
        let latestArticleCard = null;
        let latestTimestamp = 0;
        
        articleCards.forEach(card => {
            const addedDate = new Date(card.getAttribute('data-added-date'));
            if (addedDate > latestTimestamp) {
                latestTimestamp = addedDate;
                latestArticleCard = card;
            }
        });
        
        // Query the API for new articles since the last one
        const response = await fetch(`/articles/newest?guid=${latestArticleCard.getAttribute('data-guid')}`);
        const data = await response.json();
        
        // Append the new articles to the page
        data.forEach(article => {
          const articleHTML = `
            <div id="article-container" class="column is-full">
                <div class="card m-1" data-guid="${article.guid}" data-added-date="${article.added_date}">
                    <div class="card-content">
                        <div class="media">
                            <div class="media-left">
                                <figure class="image is-96x96">
                                    <img src="${article.image}" alt="Article image" style="object-fit: cover;">
                                </figure>
                            </div>
                            <div class="media-content">
                                <p class="title is-4">"${article.title}" </p>
                                <p class="subtitle is-6">by:"${article.author}"</p>
                            </div>
                        </div>

                        <div class="content">
                            "${article.synopsis}"
                            <br/>
                            Published: <time datetime="${article.published_date}">${article.published_date}</time>
                        </div>
                    </div>
                        <footer class="card-footer">
                            <a href="${article.url}"  target= "_blank" class="card-footer-item">Read More</a>
                            <a href="#" class="card-footer-item">Save</a>
                            <a href="#" class="card-footer-item">Share</a>
                        </footer>
                    </div>
                </div>`;
            // Prepend the new article HTML at the top of the container
            if (container.firstElementChild) {
                container.firstElementChild.insertAdjacentHTML('beforebegin', articleHTML);
            } else {
                container.innerHTML += articleHTML;
            }
        });
      } */
})