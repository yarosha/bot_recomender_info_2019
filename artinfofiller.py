page = requests.get('https://www.wikiart.org/en/artists-by-genre')
soup = bs(page.text, 'html.parser')
genre_name_list = soup.find_all(class_ = "dictionaries-list")[2]
genre_name_list = genre_name_list.find_all("a")
genre_painter = {}
names_ans = []
names_links = []
genre_ans = []
genre_links = []
for i in tqdm(genre_name_list):
    genre_painter[i.text.split(" ")[0]] = []
    ap = i.get("href")
    ap = "https://www.wikiart.org" + ap + "/text-list"
    print(ap)
    genre_ans.append(i.text.split(" ")[0])
    genre_links.append(ap)
    page_genre = requests.get(ap)
    soup_genre = bs(page_genre.text, 'html.parser')
    names = soup_genre.find_all(class_= "masonry-text-view masonry-text-view-all")[0]
    names = names.find_all("a")
    for j in names:
        names_ans.append(j.text)
        names_links.append("https://www.wikiart.org" + j.get("href"))
        genre_painter[i.text.split(" ")[0]].append(j.text)
fileapp = [names_ans, names_links, genre_ans, genre_links, genre_painter]
fileapp = json.dumps(fileapp)
f = open('artinfo.json', 'w')
f.write(fileapp)
f.close()
