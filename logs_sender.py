# pylint: disable=C0111
"""Dummy sender that sends log formatted data, acting as logstash output"""
import os
import multiprocessing as mp
import pika

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

def dummy_sender(filename: str, exchange: str):

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.exchange_declare(exchange=exchange, exchange_type='direct', durable=True)
    with open(os.path.join(__location__, filename), 'r', encoding='utf-8') as log_file:

        for log in log_file:
            channel.basic_publish(exchange=exchange, routing_key=exchange, body=log)
        connection.close()
    print('Sent logs in {}!'.format(filename))

if __name__ == '__main__':
    first_sender = mp.Process(
        target=dummy_sender, args=('good_logfile.log','pet-a-pet-good-logs',))
    second_sender = mp.Process(
        target=dummy_sender, args=('bad_logfile.log','pet-a-pet-bad-logs',))

    first_sender.start()
    second_sender.start()
    first_sender.join()
    second_sender.join()
