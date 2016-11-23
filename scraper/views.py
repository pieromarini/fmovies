from bs4 import BeautifulSoup
import time
import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.views import View
from django.views.generic.edit import CreateView, DeleteView
from scraper.models import Serie

BASE_URL = "http://fmovies.to"

class Index(View):
    def get(self, request):
        return render(request, 'index.html')

# Display the list of tracked series with their stored info.
class Tracker(View):
    def get(self, request):
        series = Serie.objects.all().order_by('name')
        return render(request, 'tracker.html', {'cont': series})

class Add_Series(CreateView):
    model = Serie
    fields = ['name', 'season']

    def form_valid(self, form):
        self.object = form.save(commit = False)
        # Format spaces with '+'.
        s_name = form.cleaned_data["name"].replace(' ', '+') + '+' + str(form.cleaned_data["season"])
        s_name = s_name.replace('+1', '') if s_name.endswith('+1') else s_name
        # Get info for new Entry and scrape required info.
        ep = get_last_ep(s_name)
        self.object.episode_link = ep["episode_link"]
        self.object.episode_num = ep["episode_num"]
        self.object.save()
        return super().form_valid(form)

# Change to use Ajax so page isn't refreshed and update DOM with jQuery.
class Update_Series(View):
    def post(self, request, pk):
        t = Serie.objects.get(pk = pk)
        name = (str(t.name) + ' ' + str(t.season)).replace(' ', '+')
        dt = get_last_ep(name)
        t.episode_link = dt["episode_link"]
        t.episode_num = dt["episode_num"]
        t.save()
        return redirect('scraper:tracker')

# Change to use Ajax so page isn't refreshed and update Dom with jQuery.
class Delete_Series(DeleteView):
    model = Serie
    def get_success_url(self):
        return reverse('scraper:tracker')

# AJAX search box.
class Search_Series(View):
    def get(self, request):
        search_text = ''
        return redirect('scraper:tracker')

    def post(self, request):
        search_text = request.POST['search_text']
        # Empty search box.
        if search_text == '':
            series = Serie.objects.all()
        else:
            series = Serie.objects.filter(name__contains = search_text)

        return render(request, 'seriesList-Template.html', {'cont': series})

# Request to scrape tracked series and display results
class Scraper(View):
    def get(self, request):
        s = list(Serie.objects.all().values('name', 'season'))
        s = ['{0}+{1}'.format(x['name'], str(x['season'])) for x in s]
        s = [t.replace(' ', '+').replace('0', '+', 1) \
            if not t.endswith('0') else t.replace(' ', '+') for t in s]

        s = [t.replace('+1', '') if t.endswith('+1') else t for t in s]
        cont = generate_content_dictionary(s)
        # Update database entries or create new ones.
        for k, v in cont.items():
            try:
                t = Serie.objects.get(name = v["name"])
                t.episode_link = v["episode_link"]
                t.episode_num = v["episode_num"]
                t.season = v["season"]
                t.save()
            except Serie.DoesNotExist:
                tmp = Serie(name = v["name"], episode_link = v["episode_link"],
                            episode_num = v["episode_num"], season = v["season"])
                tmp.save()

        return redirect('scraper:tracker')


class Latest_Movies(View):
    def get(self, request):
        return render(request, 'latest-movies.html')

##################################################
################ Scraping Logic ##################
##################################################

def get_last_ep(series_name):
    #prettify name
    season = '1'
    name = series_name
    if '+' in series_name:
        name, season = series_name.rsplit('+', 1)
    name = name.capitalize()
    if '+' in name:
        name = name.replace('+', ' ')
    #Scrape series url (For season)
    payload = {'keyword': series_name}
    r = requests.get('{0}/filter?sort=type%5B%5D%3Dseries&type%5B%5D=series'.format(BASE_URL), params = payload)
    soup = BeautifulSoup(r.text, 'html.parser')
    result = soup.find("a", class_ = "poster")
    result = result.get('href')
    #Scrape last episode
    r2 = requests.get('{0}{1}'.format(BASE_URL, result))
    soup2 = BeautifulSoup(r2.text, 'html.parser')
    episodes = soup2.select("ul.episodes.range.active")[0]
    last_episode_link = episodes.find_all("a")[-1].get('href')
    last_episode_num = episodes.find_all("a")[-1].text
    time.sleep(5)
    return {"name": name, "episode_num": last_episode_num,
            "episode_link": '{0}{1}'.format(BASE_URL,last_episode_link),
            "season": season,
           }

# Generate Json-Like response dict for the templates.
def generate_content_dictionary(series):
    content = {}
    for s in series:
        tmp = get_last_ep(s)
        content[tmp['name']] = tmp
    return content

