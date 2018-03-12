from django import forms
from django.forms import ModelForm

from .models import *


# blatantly stolen from
# http://stackoverflow.com/questions/5935546/align-radio-buttons-horizontally-in-django-forms?rq=1


class ResponseForm(ModelForm):
    class Meta:
        model = Response
        fields = []

    def __init__(self, *args, **kwargs):
        survey = kwargs.pop('survey')
        user = kwargs.pop('user')
        self.survey = survey
        self.user = user
        super(ResponseForm, self).__init__(*args, **kwargs)

        data = kwargs.get('data')
        for q in survey.questions():
            if q.question_type == Question.TEXT:
                self.fields["question_%d" % q.pk] = forms.CharField(label=q.text,
                                                                    widget=forms.Textarea)
            elif q.question_type == Question.RADIO:
                question_choices = q.get_choices()
                self.fields["question_%d" % q.pk] = forms.ChoiceField(label=q.text,
                                                                      widget=forms.RadioSelect,
                                                                      choices=question_choices)
            elif q.question_type == Question.SELECT:
                question_choices = q.get_choices()
                # add an empty option at the top so that the user has to
                # explicitly select one of the options
                question_choices = tuple([('', '-------------')]) + question_choices
                self.fields["question_%d" % q.pk] = forms.ChoiceField(label=q.text,
                                                                      widget=forms.Select, choices=question_choices)
            elif q.question_type == Question.SELECT_MULTIPLE:
                question_choices = q.get_choices()
                self.fields["question_%d" % q.pk] = forms.MultipleChoiceField(label=q.text,
                                                                              widget=forms.CheckboxSelectMultiple,
                                                                              choices=question_choices)
            elif q.question_type == Question.INTEGER:
                self.fields["question_%d" % q.pk] = forms.IntegerField(label=q.text)

            # if the field is required, give it a corresponding css class.
            if q.required:
                self.fields["question_%d" % q.pk].required = True
                self.fields["question_%d" % q.pk].widget.attrs["class"] = "required"
            else:
                self.fields["question_%d" % q.pk].required = False

            if q.category:
                classes = self.field["question_{}".format(q.pk)].widget.attrs.get("class")
                if classes:
                    self.field["question_{}".format(q.pk)].widget.attrs["class"] = classes + (
                    " cat_{}".format(q.category.name))
                else:
                    self.field["question_{}".format(q.pk)].widget.attrs["class"] = (" cat_{}".format(q.category.name))
            if data:
                self.fields["question_{}".format(q.pk)].initial = data.get('question_{}'.format(q.pk))

    def save(self, commit=True):
        # save the response object
        response = super(ResponseForm, self).save(commit=False)
        response.survey = self.survey
        response.user = self.user
        print("999999999999999999999999999999")
        print(self.user.is_active)
        print(response.user.is_active)
        response.save()

        # create an answer object for each question and associate it with this
        # response.
        for field_name, field_value in self.cleaned_data.items():
            if field_name.startswith("question_"):
                # warning: this way of extracting the id is very fragile and
                # entirely dependent on the way the question_id is encoded in the
                # field name in the __init__ method of this form class.
                q_id = int(field_name.split("_")[1])
                q = Question.objects.get(pk=q_id)

                if q.question_type == Question.TEXT:
                    a = AnswerText(question=q)
                    a.body = field_value
                elif q.question_type == Question.RADIO:
                    a = AnswerRadio(question=q)
                    a.body = field_value
                elif q.question_type == Question.SELECT:
                    a = AnswerSelect(question=q)
                    a.body = field_value
                elif q.question_type == Question.SELECT_MULTIPLE:
                    a = AnswerSelectMultiple(question=q)
                    a.body = field_value
                elif q.question_type == Question.INTEGER:
                    a = AnswerInteger(question=q)
                    a.body = field_value
                print("creating answer to question {} of type {}".format(q_id, a.question.question_type))

                print(a.question.text)

                print('answer value:' + field_value.__str__())
                a.response = response
                a.save()
        return response
