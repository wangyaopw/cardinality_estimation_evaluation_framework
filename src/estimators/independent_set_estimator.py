# Copyright 2020 The Private Cardinality Estimation Framework Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Estimator for sketches when using the independence assumption.

Under the independence assumption, the cardinality of the union of two
sketches representing sets A and B is equal to
   
  |A| + |B| - |A| * |B| / N,

where N is the size of the universe from which A and B are drawn.
"""

from itertools import accumulate
from wfa_cardinality_estimation_evaluation_framework.estimators.base import EstimatorBase


class IndependentSetEstimator(EstimatorBase):
  """An estimator that estimates the size of a union by assuming independence.

  Given two sketches A and B representing samples drawn from a universe U,
  the estimated size of A union B is given by:

    |A union B| = |A| + |B| - |A| * |B| / |U|.

  """

  def __init__(self, single_sketch_estimator, universe_size):
    """Instantiates an IndependentSetEstimator object.

    Args:
      single_sketch_estimator:  An object derived from EstimatorBase for
        providing cardinality estimates of individual sketches.
      universe_size: Size of the universe.
    """
    self.single_sketch_estimator = single_sketch_estimator
    self.universe_size = universe_size

  def __call__(self, sketch_list):
    """Returns the frequency histogram of a union of sketches."""
    if not sketch_list:
      return [0]
    
    a_hist = [0]  # Exact frequencies of current estimate
    for sketch in sketch_list:
      ch = self.single_sketch_estimator([sketch])
      # b_hist is the exact frequency histogram for the new sketch.
      b_hist = [ch[i] - ch[i+1] for i in range(len(ch)-1)] + [ch[-1]]

      # To compute the histogram of the union, we look at all pairs
      # A[i] and B[j], where A[i] (resp. B[j]) is the number of items with
      # frequency i+1 in A (resp. j+1 in B).  Items in the intersection
      # of A[i] and B[j] will have frequency i+j+2 in the union.
      # These items will need to be deducted from the frequency counts for
      # both i and j to avoid overcounting.
      c_hist = a_hist.copy()
      if len(c_hist) < len(b_hist):
        c_hist += [0] * (len(b_hist) - len(c_hist))
      for i in range(len(b_hist)):
        c_hist[i] += b_hist[i]
      for i in range(len(a_hist)):
        for j in range(len(b_hist)):
          overlap = a_hist[i] * b_hist[j] / self.universe_size
          if overlap:
            c_hist[i] -= overlap
            c_hist[j] -= overlap
            if len(c_hist) < i+j+2:
              c_hist += [0] * (i + j + 2 - len(c_hist))
            c_hist[i+j+1] += overlap

      a_hist = c_hist

      if sum(a_hist) > self.universe_size:
          raise ValueError("Constraint violation: sketch is larger than universe")

    # At this point, a_hist is the histogram of exact frequencies,
    # e.g., a_hist[i] is the number of items having frequency exactly i+1.
    # Now convert it into a histogram of cumulative frequencies.

    a_hist = [int(f) for f in a_hist]
    cumulative_hist = list(reversed(list(accumulate(reversed(a_hist)))))

    return cumulative_hist
