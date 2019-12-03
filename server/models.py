from django.db import models


class History(models.Model):

    id_vk = models.TextField(max_length=50)
    date = models.TextField()
    operation = models.TextField(max_length=50)
    value = models.TextField(max_length=100)
    type_costs = models.TextField(max_length=100)
    comment = models.TextField(max_length=250, blank=True)
    currency = models.TextField(max_length=3, blank=True, default='RUB')

    def __str__(self):
        return '%s - %s -  %s - %s - %s' % (self.id_vk, self.date, self.operation, self.value, self.type_costs, self.currency)


class Vkuser(models.Model):

    id_vk = models.TextField(max_length=50)
    name = models.TextField(max_length=100, blank=True)
    sure_name = models.TextField(max_length=100, blank=True)
    budget = models.TextField(max_length=100, blank=True)
    pay_day = models.TextField(blank=True)
    common = models.TextField(max_length=1000)
    fun = models.TextField(max_length=1000)
    invest = models.TextField(max_length=1000)
    days_to_payday = models.TextField(max_length=100, blank=True)
    register_date = models.TextField(max_length=100,  blank=True)
    timezone = models.IntegerField(default=0)
    currency = models.TextField(max_length=3, blank=True, default='RUB')
    is_tutorial_done = models.BooleanField(default=False)
    is_vk_theme = models.BooleanField(default=True)
    is_costom_dark_theme = models.BooleanField(default=False)
    is_full_history = models.BooleanField(default=True)

    def __str__(self):
        return '%s | %s | %s | %s' % (self.id_vk, self.budget, self.currency, self.register_date)
