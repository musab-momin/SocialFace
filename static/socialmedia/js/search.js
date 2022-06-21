//catching the form and attaching keypress event

const suggestionsDiv = document.querySelector('.search-suggestion')
const searchField = document.getElementById('search_txt')

const setSearch = (txt) => {
    searchField.value = txt
    document.getElementById('search-frm').submit()
}

const fetchSuggestions = async (searchTxt) => {
    try {
        const response = await fetch(`http://127.0.0.1:8000/search_suggestions/${searchTxt}`);
        let data = await response.json()
        data = JSON.parse(data)
        suggestionsDiv.classList.add('active')
        suggestionsDiv.innerHTML = ''
        if (data.length > 0) {
            data.map(ele => {
                suggestionsDiv.innerHTML += `
            <button class='search-suggestion-btn' onclick='setSearch(this.innerText)'>${ele.fields.username}</button>
            `
            })
        } else {
            suggestionsDiv.innerHTML = `<p class='result-404'>no result found</p>`
        }
    } catch (err) {
        suggestionsDiv.innerHTML = `<p class='result-404'>no result found</p>`
        console.err('Got this error while fetching search sugesstions', err)
    }

}

const debounce = (cb) => {
    let timer;
    return (...args) => {
        clearTimeout(timer)
        timer = setTimeout(function () {
            cb(...args)
        }, 1000)
    }

}
const betterSuggestions = debounce(fetchSuggestions);
const handleSearchSuggestions = (eve) => {
    const searchTxt = eve.target.value
    betterSuggestions(searchTxt)
}
const searchInp = document.getElementById('search_txt');
searchInp.addEventListener('keypress', handleSearchSuggestions)

window.addEventListener('click', function () {
    suggestionsDiv.classList.remove('active')
})