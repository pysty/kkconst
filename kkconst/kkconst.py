#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# @author   ZHONG KAIXIANG <xiang.ace@gmail.com>
# @date     Nov 14 2015
# @brief
#


try:
    from six import with_metaclass
except:
    def with_metaclass(meta, *bases):
        """Create a base class with a metaclass. copy from six """
        class metaclass(meta):
            def __new__(cls, name, this_bases, d):
                return meta(name, bases, d)
        return type.__new__(metaclass, 'temporary_class', (), {})

import time
import datetime

from . import util

try:
    from cached_property import cached_property
except:
    class cached_property(object):
        """ https://github.com/bottlepy/bottle/blob/master/bottle.py """
        def __init__(self, func):
            self.__doc__ = getattr(func, '__doc__')
            self.func = func

        def __get__(self, obj, cls):
            if obj is None:
                return self
            value = obj.__dict__[self.func.__name__] = self.func(obj)
            return value


class _RawConstField(object):
    SUPPORT_TYPES = (int, float, str, bytes, datetime.datetime,)
    if util.PY2:
        SUPPORT_TYPES += (unicode,)  # awesome

    _REGISTERED_FIELD_DICT = {}  # type: const_cls

    def __call__(self, base_type):
        const_field = self._REGISTERED_FIELD_DICT.get(base_type)
        if const_field:
            return const_field

        class ConstField(base_type):
            TYPE = base_type

            def __new__(const_cls, value=None, verbose_name=u"", **kwargs):
                real_value = util.get_real_value(base_type, value)

                if type(real_value) not in self.SUPPORT_TYPES:
                    raise TypeError(
                        "const field only support types={0} value={1} real_value={2}".format(
                            self._SUPPORT_TYPES, value, real_value
                        )
                    )

                if not isinstance(real_value, base_type):
                    raise TypeError(
                        "const field real_value={0} v_type={1} value={2} not match type={3}".format(
                            real_value, value, type(value), const_cls.TYPE
                        )
                    )

                if base_type is datetime.datetime:
                    kwargs["year"] = real_value.year
                    kwargs["month"] = real_value.month
                    kwargs["day"] = real_value.day
                    kwargs["hour"] = real_value.hour
                    kwargs["minute"] = real_value.minute
                    kwargs["second"] = real_value.second
                    kwargs["microsecond"] = real_value.microsecond
                    kwargs["tzinfo"] = real_value.tzinfo
                    obj = datetime.datetime.__new__(const_cls, **kwargs)
                else:
                    obj = base_type.__new__(const_cls, real_value)
                    obj.__dict__.update(**kwargs)
                obj.verbose_name = verbose_name
                return obj

        self._REGISTERED_FIELD_DICT[base_type] = ConstField
        return ConstField

    @property
    def registered_field_types(self):
        return list(self._REGISTERED_FIELD_DICT.values())


_ConstField = _RawConstField()


class _Mixin(object):
    # just for ide code intellisense :)
    TYPE = NotImplemented
    verbose_name = NotImplemented


# number
class ConstIntField(_ConstField(int), _Mixin):
    """ no support long type, the const value <= sys.maxint at PY2"""


class ConstFloatField(_ConstField(float), _Mixin):
    pass


# str/unicode
class ConstStringField(_ConstField(str), _Mixin):
    pass

if util.PY2:
    ConstBytesField = ConstStringField

    class ConstUnicodeField(_ConstField(unicode), _Mixin):
        pass
else:
    class ConstBytesField(_ConstField(bytes), _Mixin):
        pass

    ConstUnicodeField = ConstStringField


# datetime
class ConstDatetimeField(_ConstField(datetime.datetime), _Mixin):
    FORMATS = util.DATETIME_FORMATS

    @cached_property
    def timestamp(self):
        return time.mktime(self.timetuple())

    def to_dict(self):
        return dict(
            year=self.year, month=self.month, day=self.day,
            hour=self.hour, minute=self.minute, second=self.second,
            microsecond=self.microsecond, tzinfo=self.tzinfo
        )


class ConstMetaClass(type):
    def __new__(cls, name, bases, namespace):
        verbose_name_dict = {}
        const_field_types = tuple(_ConstField.registered_field_types)
        for k, v in namespace.items():
            # just check base const field by _ConstFieldHelper.get_const_filed_class(xxx)
            if getattr(v, '__class__', None) and isinstance(v, const_field_types):
                verbose_name_dict[v] = getattr(v, 'verbose_name', "")
        namespace["_verbose_name_dict"] = verbose_name_dict
        return type.__new__(cls, name, bases, namespace)

    def __setattr__(self, key, value):
        raise AttributeError("Could not set ConstField {key} {value} again".format(key=key, value=value))


class BaseConst(with_metaclass(ConstMetaClass)):
    """ Abstract Class """
    _verbose_name_dict = NotImplemented

    @classmethod
    def get_verbose_name(cls, const_value, default=None):
        return cls._verbose_name_dict.get(const_value, default)
