from boards.models import Blogger, Reader
from logging import exception

def get_avatar(request):
    if request.user.is_authenticated:
        try:
            avatar_image = Blogger.objects.filter(user=request.user).first()
            if avatar_image is None:
                raise exception
        except :
            avatar_image =  Reader.objects.filter(user=request.user).first()
        return {
            'avatar_image':avatar_image
            }
    else:
        return {
            'avatar_image':None
            }

