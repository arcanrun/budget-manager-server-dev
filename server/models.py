from django.db import models


class History(models.Model):

    id_vk = models.TextField(max_length=50)
    date = models.TextField()
    operation = models.TextField(max_length=50)
    value = models.TextField(max_length=100)
    type_costs = models.TextField(max_length=100)

    def __str__(self):
        return '%s - %s -  %s - %s - %s' % (self.id_vk, self.date, self.operation, self.value, self.type_costs)


class Vkuser(models.Model):

    id_vk = models.TextField(max_length=50)
    budget = models.TextField(max_length=100)
    pay_day = models.TextField()
    common = models.TextField(max_length=1000)
    fun = models.TextField(max_length=1000)
    invest = models.TextField(max_length=1000)
    days_to_payday = models.TextField(max_length=100)
    register_date = models.TextField(max_length=100)

    def __str__(self):
        return 'id_vk--->%s || budget--->%s' % (self.id_vk, self.budget)
