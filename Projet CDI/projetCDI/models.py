from django.db import models


class Livre(models.Model):
    isbn = models.CharField(max_length=14, primary_key=True)
    siret = models.IntegerField()
    titre = models.CharField(max_length=300)
    annee = models.IntegerField()

    class Meta:
        db_table = 'Livre'


class Emprunt(models.Model):
    isbn = models.CharField(max_length=14, primary_key=True)
    num_etu = models.IntegerField()
    date_ret = models.DateField()

    class Meta:
        db_table = 'Emprunt'


class Eleve(models.Model):
    num_etu = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=90)
    prenom = models.CharField(max_length=90)
    classe = models.CharField(max_length=90)

    class Meta:
        db_table = 'Eleve'


class Editeur(models.Model):
    siret = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=90)

    class Meta:
        db_table = 'Editeur'


class Ecrire(models.Model):
    a_id = models.ForeignKey('Auteur', on_delete=models.CASCADE)
    isbn = models.ForeignKey('Livre', on_delete=models.CASCADE)

    class Meta:
        unique_together = (('a_id', 'isbn'),)
        db_table = 'Ecrire'


class Auteur(models.Model):
    a_id = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=200)

    class Meta:
        db_table = 'Auteur'
