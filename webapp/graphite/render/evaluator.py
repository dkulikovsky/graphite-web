import datetime
import time
from django.conf import settings
from graphite.render.grammar import grammar
from graphite.logger import log
from graphite.render.datalib import fetchData, fetchDataMulti, TimeSeries


def evaluateTargets(requestContext, targets):
    tokens = []
    for target in targets:
        tokens.append(grammar.parseString(target))

    result = evaluateTokensMulti(requestContext, tokens)

    if isinstance(result, TimeSeries):
        return [result]  # we have to return a list of TimeSeries objects

    return result


def findPaths(requestContext, tokens, paths):
    if tokens.expression:
        findPaths(requestContext, tokens.expression, paths)
    elif tokens.call:
        for arg in tokens.call.args:
            findPaths(requestContext, arg, paths)
        for kwarg in tokens.call.kwargs:
            findPaths(requestContext, kwarg.args[0], paths)
    elif tokens.pathExpression:
        paths.add(tokens.pathExpression)


def evaluateTokensMulti(requestContext, tokensList):
    fetch = set()
    result = [ ]

    for tokens in tokensList:
        findPaths(requestContext, tokens, fetch)

    timeSeriesList = fetchDataMulti(requestContext, list(fetch))
    series = []
    for tokens in tokensList:
        serie = evaluateTokensWithTimeSeries(requestContext, tokens, timeSeriesList)
        if isinstance(serie, TimeSeries):
            series.append(serie)
        else:
            series.extend(serie)

    return series


def evaluateTokensWithTimeSeries(requestContext, tokens, timeSeriesList):
    if tokens.expression:
        return evaluateTokensWithTimeSeries(requestContext, tokens.expression, timeSeriesList)

    elif tokens.pathExpression:
        for ts in timeSeriesList:
            print('%s == %s is %s' % (ts.name, tokens.pathExpression, ts.name == tokens.pathExpression))
            if ts.name == tokens.pathExpression:
                return [ts]
        fetch = fetchDataMulti(requestContext, [tokens.pathExpression])
        if isinstance(fetch, list):
            return fetch
        return [fetch]

    elif tokens.call:
        func = SeriesFunctions[tokens.call.func]
        args = [evaluateTokensWithTimeSeries(requestContext,
                               arg,
                               timeSeriesList) for arg in tokens.call.args]
        kwargs = dict([(kwarg.argname,
                        evaluateTokensWithTimeSeries(requestContext,
                                      kwarg.args[0],
                                      timeSeriesList))
                       for kwarg in tokens.call.kwargs])
        return func(requestContext, *args, **kwargs)

    elif tokens.number:
        if tokens.number.integer:
            return int(tokens.number.integer)
        elif tokens.number.float:
            return float(tokens.number.float)
        elif tokens.number.scientific:
            return float(tokens.number.scientific[0])

    elif tokens.string:
        return tokens.string[1:-1]

    elif tokens.boolean:
        return tokens.boolean[0] == 'true'

def evaluateTarget(requestContext, target):
  tokens = grammar.parseString(target)
  result = evaluateTokens(requestContext, tokens)

  if type(result) is TimeSeries:
    return [result] #we have to return a list of TimeSeries objects

  else:
    return result


def evaluateTokens(requestContext, tokens):
  if tokens.expression:
    return evaluateTokens(requestContext, tokens.expression)

  elif tokens.pathExpression:
    return fetchData(requestContext, tokens.pathExpression)

  elif tokens.call:
    try:
      func = SeriesFunctions[tokens.call.func]
      args = [evaluateTokens(requestContext, arg) for arg in tokens.call.args]
      return func(requestContext, *args)
    except ValueError:
      log.exception('value error when render') 
      return []

  elif tokens.number:
    if tokens.number.integer:
      return int(tokens.number.integer)
    elif tokens.number.float:
      return float(tokens.number.float)
    elif tokens.number.scientific:
      return float(tokens.number.scientific[0])

  elif tokens.string:
    return tokens.string[1:-1]

  elif tokens.boolean:
    return tokens.boolean[0] == 'true'


#Avoid import circularities
from graphite.render.functions import SeriesFunctions
