from aiohttp import web
import json
routes = web.RouteTableDef()


users = {}
user_id = 1


@routes.get('/')
async def handle(request):
    response_obj = {'status': 'Welcome to the demo aiohttp API'}
    return web.Response(text=json.dumps(response_obj))


@routes.get('/users')
async def get_users(request):
    response_obj = {'users': [users]}
    return web.Response(text=json.dumps(response_obj))


@routes.get('/users/{user_id}')
async def get_user(request):
    user_id = int(request.match_info.get('user_id'))
    # print(user_id, type(user_id))
    # print(list(users.keys()), type(list(users.keys())[0]))
    if user_id in list(users.keys()):
        response_obj = {'user': users[user_id]}
        return web.Response(text=json.dumps(response_obj))
    else:
        return web.Response(text='User not found', status=404)


@routes.post('/users')
async def new_user(request):

    global user_id
    global users
    try:
        data = await request.json()
        users[user_id] = data
        response_obj = {'status': 'success',
                        'message': 'user created successfully', 'user': [users[user_id]]}
        user_id += 1
        return web.Response(text=json.dumps(response_obj), status=201)
    except Exception as e:
        err_msg = {'status': 'error', 'message': str(e)}
        return web.Response(text=json.dumps(err_msg), status=500)


@routes.put('/users/{user_id}')
async def update_user(request):
    user_id = int(request.match_info.get('user_id'))

    try:
        data = await request.json()
        if user_id in list(users.keys()):
            users[user_id] = data
            response_obj = {'status': 'success',
                            'message': 'user updated successfully', 'user': [users[user_id]]}
            return web.Response(text=json.dumps(response_obj), status=200)
        else:
            return web.Response(text=json.dumps({'status': 'error', 'message': 'user not found'}), status=404)
    except Exception as e:
        err_msg = {'status': 'error', 'message': str(e)}
        return web.Response(text=json.dumps(err_msg), status=500)


@routes.delete('/users/{user_id}')
async def delete_user(request):
    user_id = int(request.match_info.get('user_id'))
    if user_id in list(users.keys()):
        del users[user_id]
        response_obj = {'status': 'success',
                        'message': 'user deleted successfully'}
        return web.Response(text=json.dumps(response_obj), status=200)
    else:
        return web.Response(text=json.dumps({'status': 'error', 'message': 'user not found'}), status=404)

app = web.Application()
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app)
