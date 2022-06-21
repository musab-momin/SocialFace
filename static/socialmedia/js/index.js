// parentDiv = document.getElementById('suggestions-parent')
// document.getElementById('btn').addEventListener('click', async(eve)=>{
//     eve.preventDefault();
//     const response = await fetch('http://127.0.0.1:8000/refresh_suggestions')
//     let data = await response.json();
//     data = JSON.parse(data)
//     data.map(ele=>{
//         console.log(ele);
//     })
// })

const modal = document.getElementById("myModal");
const contentDiv = document.querySelector('.comments-sec')

const fetchComments = async (post_id) => {
    modal.style.display = "block";
    console.log(post_id);

    const activePost = document.getElementById(post_id)
    const activePostProfileImage = activePost.children[0].children[0].children[0].children[0].src;
    const activePostImage = activePost.children[1].src;
    const activePostName = activePost.children[0].children[0].children[1].children[0].innerHTML.trim()
    const activePostCaption = activePost.children[2].children[2].children[1].innerHTML.trim()

    document.getElementById('active-post-img').src = activePostImage
    document.getElementById('active-post-profile-img').src = activePostProfileImage
    document.getElementById('comment-name').innerHTML = activePostName+':'
    document.getElementById('active-post-caption').innerText = activePostCaption
    
    const response = await fetch(`http://127.0.0.1:8000/fetch_comments/${post_id}`)
    let data = await response.json()
    data = JSON.parse(data)
    contentDiv.innerHTML = ""
    if (data.length > 0){
        data.forEach(ele=>{
            console.log(ele);
            contentDiv.innerHTML += `
            <div class="content-div__comments">
            <div class="content-div__comment" style="margin: 1em 0;">
                <div class="post-sec">
                    <p id="comment-name">${ele.fields.commented_by}:</p>
                    <p>${ele.fields.content} <br /><button class="like-btn">${ele.fields.number_of_likes} likes</button> </p>
                </div>
            </div>
            
            
        </div>
            `
        })
    }
    else{
        contentDiv.innerHTML = `<h3>Nobody yet commented on your post!</h3>`
    }
   

}
// When the user clicks anywhere outside of the modal, close it
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
}
