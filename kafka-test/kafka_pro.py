import time
from kafka import KafkaProducer
from multiprocessing import Process


MAX = 50
kafka_list = ['192.168.1.139:9092', '192.168.1.140:9092', '192.168.1.152:9092']
# producer = KafkaProducer(bootstrap_servers=['192.168.1.139:9092', '192.168.1.140:9092'])
# producer = [KafkaProducer(bootstrap_servers=kafka_list)] * MAX

topic = [0]*MAX

for x in range(0, MAX):
    topic[x] = 'box{}'.format(x)

base = '232303FE{}030160327015264398FB69A77D318B3F3D2FBF11763D8E0402AB88C579BAC7182998EB48439507243CF8631BAA7CBEE016E4F42F03B7E3D27E76B610683369065A8AEB4EB7A74C51DCA3DDE16BC02FDDB0A49B0C8B227B5D06AAA757C3A7D5832C2D3B01D6554E1A1FA413C968BC074613221AD5BC17161DEEC4F58131E13D1C35F52F20D2888525689AD570A57590646ECFF3352ECF4CDE5609E3C03D990B4C34F860B60D26AC4F5EE4632E3C64BDDB13B7F1D9A2A75AE43CA3770A1EF584D824312068CBE444328D7B390AEF4C5CD005C04F6505298AF34DC448F18525F1AA6D1B299E2C849BE1B54DD4FF495CD8CAB71BB325B8C17C3E56273375FBBFBDB0991837B2EE146D65985F72C2080FF49CADEC79652E676C2C59A9A17D161AE1DAE6D41FCC3F0AC65546C98DA401C49A7B4E426AEA54EFE2DB3C692B7EEC534D5FE976E49FE2482E06702284F58672E84D80BAB47D8BF12BF106ECCC5B6C60D74F9D4BDDA2'
send_data = [base] * MAX
vin = ['4C44504141414B433848433130373837{}'] * MAX
for x in range(0, MAX):
    num = '%02x' % x
    vin[x] = vin[x].format(num)
    send_data[x] = base.format(vin[x])
    vin[x] = bytes(vin[x], 'utf-8')
    send_data[x] = bytes(send_data[x], 'utf-8')


def get_index(md5):
    index = 0
    for x in md5:
        index += ord(x)
    index = index % MAX
    return index


def test_send(id, times):
    producer = KafkaProducer(bootstrap_servers=kafka_list)
    print('{} begin'.format(id))
    for x in range(0, times):
        producer.send(topic[id], send_data[id])
    print('{} done'.format(id))


# 25 * 2880 * 400    5185.024734020233 s
# 25 * 2880 * 1000
def thread_all():
    thread_list = [0]*MAX
    total = 2880*1000*25
    for x in range(0, MAX):
        thread_list[x] = (Process(target=test_send, args=(x, int(total/MAX))))
        thread_list[x].start()
    for x in range(0, MAX):
        thread_list[x].join()


if __name__ == '__main__':
    dt = time.time()
    thread_all()
    dt = time.time()-dt
    print(dt)
