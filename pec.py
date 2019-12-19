import time
import heapq

def make_cache_item(key, val, pnode, enode):
	return {'k': key, 'v': val, 'p': pnode, 'e':enode}

def make_pnode(priority, last_used, ptr):
	return [priority, last_used, ptr]

def make_enode(expire, ptr):
	return [expire, ptr]

cache_items = {}
heap_expiry = []
heap_priority = []

#assuming the size of the cache is max 5
cache_size = 5

#assuming the expiry time is an epoch timestamp
currTime = time.time()
def evict():
	if len(heap_expiry) == 0:
		return 0
	while heap_expiry[0][0] < currTime:
		removeExpiry()

#helper function to clean up nodes from difference placess
def removePriority():
	if len(heap_priority) == 0:
		return 0

	val = heapq.heappop(heap_priority)
	#now need to also remove val from cache items and from other heap (expiry)
	heap_expiry.remove(val[2]['e'])
	heapq.heapify(heap_expiry)
	del cache_items[val[2]['k']]

def removeExpiry():
	if len(heap_expiry) == 0:
		return 0
	val = heapq.heappop(heap_expiry)
	#now need to also remove val from cache items and from other heap (expiry)
	heap_priority.remove(val[2]['e'])
	heapq.heapify(heap_priority)
	del cache_items[val[2]['k']]



def get(key):
	evict()
	val = cache_items.get(key, default = None)
	#update the used time
	if val is not None:
		val['p'][1] = time.time()
		heapq.heapify(heap_priority)
		return val['v']

	return None


def set(key, value, priority, expiry):
	evict()
	if key in cache_items:
		#update the values 
		cache_items[key]['p'][0] = priority
		cache_items[key]['p'][1] = time.time()

		cache_items[key]['e'][0] = expiry
		cache_items[key]['v'] = value

		#update the heap after updating values 
		heapq.heapify(heap_expiry)
		heapq.heapify(heap_priority)

	else:
			#insert key into dictionary
			cache_items[key] = make_cache_item(key, value, None, None)
			pnode = make_pnode(priority, time.time(), cache_items[key])
			enode = make_enode(expiry, cache_items[key])
			cache_items[key]['p'] = pnode
			cache_items[key]['e'] = enode

			#putting the node into its respective heap
			heapq.heappush(heap_expiry, enode)
			heapq.heappush(heap_priority, pnode)

			if len(cache_items) >= cache_size:
				removePriority()