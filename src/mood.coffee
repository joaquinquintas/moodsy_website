getIdFromUrl = () ->
  parts = String(window.location).split("/")
  last = parts.pop()
  if not last
    last = parts.pop()
  return last

fetchMoodData = (id) ->
  url = "http://dev.moodsy.me/2/public/post/" + id + "/"
  req = new XMLHttpRequest()
  req.open('GET', url, true)

  req.onload = () ->
    if req.status >= 200 and req.status < 400
      injectData JSON.parse(req.responseText)
      # XXX: Load + call some emoji lib? :)
    else
      # Internal moodsy error
      console.log "err"

  req.onerror = () ->
    # Network error
    console.log "neterr"

  req.send()

moodsyMoment = (date) ->
  return moment(date, 'YYYY-MM-DD HH:mm:ss Z')

q = (selector) ->
  return document.querySelectorAll(selector)

appendHeart = (heart, parent) ->
  moodsy = document.createElement('a')
  moodsy.href = '/app'
  moodsy.innerHTML = heart.user_fname
  parent.appendChild(moodsy)


injectData = (data) ->
  post_date = moodsyMoment(data.post.datetime)

  q('#status .name')[0].innerHTML = data.profile.name
  q('#status date')[0].innerHTML = post_date.fromNow()
  q('#status date')[0].title = post_date.format()
  q('#status .text')[0].innerHTML = data.post.description.text
  q('#mood img')[0].src = data.post.image_url
  q('#status .avatar img')[0].src = data.profile.profile_img

  heartParent = q('#likes p')[0]
  if data.moodsies.moodsies.length > 0
    last = data.moodsies.moodsies.pop()
  if data.moodsies.moodsies.length > 0
    second_last = data.moodsies.moodsies.pop()
  if data.moodsies.moodsies.length > 0
    for entry in data.moodsies.moodsies
      appendHeart(entry, heartParent)
      heartParent.appendChild(document.createTextNode(', '))

  if second_last
    appendHeart(second_last, heartParent)
    heartParent.appendChild(document.createTextNode(' and '))

  if last
    appendHeart(last, heartParent)
    heartParent.insertBefore(document.createTextNode('By: '), heartParent.firstChild)
  else
    heartParent.appendChild(document.createTextNode('No one.'))

  commentTmpl = q('#comments .comment')[0]
  if data.comments.comments.length > 0
    for comment in data.comments.comments
      commentNode = commentTmpl.cloneNode(true)
      commentNode.querySelectorAll('.avatar img')[0].src = comment.profile_img
      commentNode.querySelectorAll('.author a')[0].innerHTML = comment.user_fname
      commentNode.querySelectorAll('.text')[0].innerHTML = comment.text
      q('#comments')[0].appendChild(commentNode)
      commentNode.style.display = ''



id = getIdFromUrl()
data = fetchMoodData(id)
