import urllib
import urllib2
import base64
import socket
import json

import util as util

socket.setdefaulttimeout(40)

class API:

    def getShowBanner(self, id):
        url = util.plugin.getSetting('url') + 'showPoster/?show=' + str(id) + '&which=banner'
        return url

    def getShowPoster(self, id):
        url = util.plugin.getSetting('url') + 'showPoster/?show=' + str(id) + '&which=poster'
        return url
    
    def getShowPosterThumbnail(self, id):
        url = util.plugin.getSetting('url') + 'showPoster/?show=' + str(id) + '&which=poster_thumb'
        return url
    

    def request(self, cmd, params = {}):
        params['cmd'] = cmd
        url = util.plugin.getSetting('url') + 'api/' + util.plugin.getSetting('key') + '/?' + urllib.urlencode(params)
        util.log('API: ' + url)
        req = urllib2.Request(url)
        user = util.plugin.getSetting('user')
        password = util.plugin.getSetting('password')
        if user and password:
            auth = base64.encodestring('{0}:{1}'.format(user, password)).replace('\n', '')
            req.add_header("Authorization", "Basic %s" % auth)        
        result = json.load(urllib2.urlopen(req))
        #util.log(result)
        if result['result'] == 'denied':
            raise Exception('Access denied, check API Key.')
        if not result['result'] == 'success':
            util.log('API Exception: ' + result['result'])
            import pprint
            pp = pprint.PrettyPrinter()
            util.log(pp.pformat(result))
        return result
    
    def getShow(self, id):
        result = self.request('show', {'tvdbid': id})
        return result['data']

    def getSeasons(self, id, params = {}):
        params['tvdbid'] = id
        result = self.request('show.seasons', params)
        return result['data']

    def getSeasonList(self, id, params = {}):
        params['tvdbid'] = id
        result = self.request('show.seasonlist', params)
        return result['data']

    def setShowPause(self, id, pause):
        return self.request('show.pause', {'tvdbid': id, 'pause': 1 if pause else 0})
    
    def doShowDelete(self, id):
        return self.request('show.delete', {'tvdbid': id})
        
    def getShows(self, params = {}):
        result = self.request('shows', params)
        return result['data']

    def getFuture(self, params = {}):
        result = self.request('future', params)
        return result['data']
        
    def getHistory(self, params = {}):
        result = self.request('history', params)
        return result['data']
        
    def getBacklog(self, params = {}):
        result = self.request('backlog', params)
        return result['data']
        
    def getFailed(self, params = {}):
        result = self.request('failed', params)
        return result['data']
        
    def doForceSearch(self):
        return self.request('sb.forcesearch')
    
    def doSearch(self, name, indexer):
        if indexer == 0:
            result = self.request('sb.searchindexers', {'name': name})
        elif indexer == 1:
            result = self.request('sb.searchtvdb', {'name': name})
        elif indexer == 2:
            result = self.request('sb.searchtvrage', {'name': name})
        else:
            return []
        return result['data']['results']
        
    def getRootDirs(self):
        result = self.request('sb.getrootdirs')
        return result['data']

    def getDefaults(self):
        result = self.request('sb.getdefaults')
        return result['data']
        
    def doAddNewShow(self, id, indexer, location, status, flattenFolders, anime, sceneNumbered, quality):
        return self.request('show.addnew', {
            'indexerid': id,
            indexer + 'id': id,
            'location': location,
            'status': status,
            'flatten_folders': 0 if flattenFolders else 1,
            'anime': 1 if anime else 0,
            'scene': 1 if sceneNumbered else 0,
            'initial': quality
        })
        
    def doEpisodeSetStatus(self, id, season, episode, status):
        return self.request('episode.setstatus', {
            'indexerid': id,
            'season': season,
            'episode': episode,
            'status': status
        })
        