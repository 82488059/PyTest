import time
from pykafka import KafkaClient
from multiprocessing import Process

MAX = 50
host = '192.168.1.139:9092, 192.168.1.140:9092, 192.168.1.152:9092'
client = [KafkaClient(hosts=host)] * MAX
topic_name = [0]*MAX
file_name = [0]*MAX
base = '232303FE{}030160327015264398FB69A77D318B3F3D2FBF11763D8E0402AB88C579BAC7182998EB48439507243CF8631BAA7CBEE016E4F42F03B7E3D27E76B610683369065A8AEB4EB7A74C51DCA3DDE16BC02FDDB0A49B0C8B227B5D06AAA757C3A7D5832C2D3B01D6554E1A1FA413C968BC074613221AD5BC17161DEEC4F58131E13D1C35F52F20D2888525689AD570A57590646ECFF3352ECF4CDE5609E3C03D990B4C34F860B60D26AC4F5EE4632E3C64BDDB13B7F1D9A2A75AE43CA3770A1EF584D824312068CBE444328D7B390AEF4C5CD005C04F6505298AF34DC448F18525F1AA6D1B299E2C849BE1B54DD4FF495CD8CAB71BB325B8C17C3E56273375FBBFBDB0991837B2EE146D65985F72C2080FF49CADEC79652E676C2C59A9A17D161AE1DAE6D41FCC3F0AC65546C98DA401C49A7B4E426AEA54EFE2DB3C692B7EEC534D5FE976E49FE2482E06702284F58672E84D80BAB47D8BF12BF106ECCC5B6C60D74F9D4BDDA2'
send_data = [base] * MAX
vin = ['4C44504141414B433848433130373837{}'] * MAX

for x in range(0, MAX):
    topic_name[x] = 'box{}'.format(x)
    num = '%02x' % x
    vin[x] = vin[x].format(num)
    send_data[x] = base.format(vin[x])
    vin[x] = bytes(vin[x], 'utf-8')
    send_data[x] = bytes(send_data[x], 'utf-8')
    file_name[x] = 'g:/data/box{}.txt'.format(x)


def test_send(id, qs, times):
    count = 0
    print('test_send {} begin'.format(id))
    client = [KafkaClient(hosts=host)] * qs
    topic_name = [0] * qs
    topic = [0]*qs
    data = [0]*qs
    pro = [0]*qs
    for n in range(0, qs):
        index = qs * id + n
        topic_name[n] = 'box{}'.format(index)
        print(topic_name[n])
        data[n] = send_data[index]
        topic[n] = client[n].topics[topic_name[n].encode()]
        pro[n] = topic[n].get_producer()

    for x in range(0, times):
        for n in range(0, qs):
            pro[n].produce(data[n])
            count += 1
            if count % 2880000 == 0:
                print('{} send {}'.format(id, times))
    print('test_send {} done {}'.format(id, count))


def test_read(id, qs, times):
    print('test_read {} begin'.format(id))
    count = 0
    topic_name = [0] * qs
    topic = [0] * qs
    file = [0] * qs
    con = [0] * qs
    for n in range(0, qs):
        index = qs * id + n
        topic_name[n] = 'box{}'.format(index)
        print(topic_name[n])
        topic[n] = client[n].topics[topic_name[n].encode()]
        con[n] = topic[n].get_simple_consumer(bytes(topic_name[n], 'utf-8'), reset_offset_on_start=True, consumer_timeout_ms=3000)
        file[n] = open(file_name[index], 'wb')

    for x in range(0, times):
        for n in range(0, qs):
            txt = con[n].consume()
            if txt is None:
                break
            file[n].write(txt.value)
            file[n].write(bytes("\r\n", 'utf-8'))
            count += 1
            if count % 2880000 == 0:
                print('{} read {}'.format(id, times))
    for n in range(0, qs):
        file[n].close()
    print('test_read {} done {}'.format(id, count))
    return None


# 25 * 2880 * 400    5185.024734020233s
# 25 * 2880 * 1000  553.0806050300598s
def thread_all():
    print('all thread begin')
    total = 2880*1000*50
    thread_list = [0]*MAX
    thread_size = 10
    queue = int(MAX/thread_size)
    times = int(total/thread_size/queue)
    for x in range(0, thread_size):
        thread_list[x] = (Process(target=test_read, args=(x, queue, times)))
        thread_list[x].start()
    for x in range(0, thread_size):
        thread_list[x].join()
    print('all thread end')


if __name__ == '__main__':
    print(time.time())
    dt = time.time()
    thread_all()
    dt = time.time()-dt
    print(dt)

