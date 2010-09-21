# PMS plugin framework
import datetime,re


##################################################################################################TBS
VIDEO_PREFIX     = "/video/TBS"
NAME          = L('Title')

TBS_URL                     = "http://www.tbs.com"
TBS_FULL_EPISODES_SHOW_LIST = "http://www.tbs.com/video/navigation/getCollections.jsp?oid=185669"

TBS_FEED                    = "http://www.TBS.com/"
DEBUG                       = False
TBSart                      ="art-default.jpg"
TBSthumb                    ="icon-default.jpg"

####################################################################################################

def Start():
  Plugin.AddPrefixHandler(VIDEO_PREFIX, VideoMainMenu, 'TBS',TBSthumb,TBSart)
  Plugin.AddViewGroup("InfoList", viewMode="InfoList", mediaType="items")
  Plugin.AddViewGroup("List", viewMode="List", mediaType="items")
  
  MediaContainer.art        =R(TBSart)
  MediaContainer.title1     = NAME
  DirectoryItem.thumb       =R(TBSthumb)

####################################################################################################
#def VideoMainMenu():
#    dir = MediaContainer(mediaType='video') 
#    dir.Append(Function(DirectoryItem(all_shows, "All Shows"), pageUrl = TBS_FULL_EPISODES_SHOW_LIST))
#    return dir
    
####################################################################################################
def VideoMainMenu():
    pageUrl=TBS_FULL_EPISODES_SHOW_LIST
    dir = MediaContainer(viewGroup="List")
    content1 = XML.ElementFromURL(pageUrl, isHTML="True")
    showMap = dict()
    shownum=0
    for thingies in content1.finall('//a[@class="topnav yesquery"]'):
          shownum =shownum+1
          showID=shownum
          Log(thingies)
          title=thingies.text
          showID=showID=re.compile('cid=([0-9]+)').findall(pageUrl)[0]
          titleUrl="http://www.tbs.com/video/navigation/getCollectionById/?oid="+showID
          Log(titleUrl)
          Log(title)
      #  Log(thumb)
          showList = showMap.get(title)
          if showList == None:
		      showList = []
		      showMap[title] = showList
		  # Tuple order here matters
          showList.append((showID,titleUrl, thumb, title))
          Log(showList)
    shows=showMap.keys()
    Log(shows)
    shows.sort()
    Log(shows)
    shownum=0
    #for shownames in shows:
    #  shownum=shownum+1
    #  showList.append((shownum,shownames.titleUrl,shownames.thumb, shownames.title))
    for showkey in shows:
      Log(showkey)
      for show in showMap[showkey]:
        Log(show)
        title=show[3]
        url=show[1]
        thumb=show[2]
        Log("Show: " + title + " | link: " + url)
        dir.Append(Function(DirectoryItem(showxml, title=title), pageUrl = url))
      
    
    return dir 

####################################################################################################
def showxml(sender, pageUrl):
  dir = MediaContainer(title2=sender.itemTitle, viewGroup="InfoList", noCache=True)
  showID=re.compile('cid=([0-9]+)').findall(pageUrl)[0]
  link="http://www.tbs.com/video/navigation/getCollectionById/?oid=" + showID
  shows=XML.ElementFromURL(link).xpath('//episode')
  for show in shows:
    
    #episodeID  
    epID=show.get('id')[0].text
    Log(epID)

    #title
    title=show.xpath('./title')[0].text
    Log(title)

    #thumb
    thumb=show.xpath('./thumbnailUrl')[0].text
    #summary
    summary=show.xpath('./description')[0].text
    clip="http://www.tbs.com/cvp/index.jsp?oid=" + epID 
    Log("link: " + clip)   
    
    
##########   This section knows the location of the flv file, but the stream is rtmpe
##########   I am keeping the code in here so it doesn't get lost so when     
#    vidlink="http://www.tnt.tv/video_cvp/cvp/videoData/?id=" + epID
#    showLinks=XML.ElementFromURL(vidlink).xpath('//video/files/file[@type="hd"]')
#    Log("++++++++++++++")
#    clip=showLinks[0].text.replace("/tveverywhere","")
#    vidname=clip.split("/")[-1]
#    date1=clip.split("/")[-2]
#    date2=date1.split("-")[-1]
#    date3=date1.split("-")[-2]
#    clip="/flash/" + date2 + "-" + date3 + "/" + vidname
#    
#    Log(clip)
#    player="http://i.cdn.turner.com/xslo/cvp/player/cvp_1.3.6.24.swf?player=fw_main&domId=cvp_1&playerWidth=640&playerHeight=360"



    dir.Append(WebVideoItem(clip, title=title, thumb=thumb, summary=summary))
    Log("epID: " + epID + " | title: " + title + " | thumb: " + thumb + " | Description: " + summary)
    
  
  return dir
