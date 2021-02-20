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
"""Tests for wfa_cardinality_estimation_evaluation_framework.estimators.dense_tail_liquid_legions."""

from absl import logging
from absl.testing import absltest

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import farmhash
import numpy

from wfa_cardinality_estimation_evaluation_framework.estimators import dense_tail_liquid_legions


class DenseTailLiquidTest(absltest.TestCase):

  def simulate_one_case(self, a, m, reach, k, trails):
    kth_inactive_register = 0
    kth_nondestroyed_register = 0
    for i in range(trails):
      s = dense_tail_liquid_legions.DenseTailLiquidLegions(a, m, random_seed=42)
      s.add_ids(list(range(reach*i, reach*(i+1))))
      kth_inactive_register = max(s.kth_inactive_register(k), kth_inactive_register)
      kth_nondestroyed_register = max(s.kth_nondestroyed_register(k),kth_nondestroyed_register)
    result = dict()
    result['kth_inactive_register_percentage'] = kth_inactive_register/m*100
    result['kth_nondestroyed_register_percentage'] = kth_nondestroyed_register/m*100
    return result



  def ttest_expected_active_register_percentage(self):
    print("hello world")
    reach = [100,1000, 10_000, 100_000, 1000_000, 10_000_000, 100_000_000, 1000_000_000]
    expected_active_register_pecentage = [0] * len(reach)

    a = 12
    m = 100_000
    s = dense_tail_liquid_legions.DenseTailLiquidLegions(a, m, random_seed=42)
    for i in range(len(reach)):
      expected_active_register_pecentage[i] = s.legions_expectation(reach[i]/m)*100
    print(reach)
    print(expected_active_register_pecentage)


  def ttest_play_ground(self):
    print("hello world")
    reach = [1000, 2000, 5000, 10_000, 20_000, 50_000, 100_000, 200_000, 500_000, 1000_000, 2_000_000, 5_000_000, 10_000_000]
    kth_inactive_register_percentage = [0] * len(reach)
    kth_nondestroyed_register_percentage = [0] * len(reach)
    expected_active_register_pecentage = [0] * len(reach)

    a = 12
    m = 100_000
    s = dense_tail_liquid_legions.DenseTailLiquidLegions(a, m, random_seed=42)
    trails = 5


    k = 1
    for i in range(len(reach)):
      print(reach[i])
      d = self.simulate_one_case(a, m, reach[i],k, trails)
      kth_inactive_register_percentage[i] = d['kth_inactive_register_percentage']
      kth_nondestroyed_register_percentage[i] = d['kth_nondestroyed_register_percentage']
      expected_active_register_pecentage[i] = s.legions_expectation(reach[i]/m)*100
    plt.subplot(121)
    plt.plot(reach,kth_inactive_register_percentage,'-b*',label=f"1st inactive register percentage")
    plt.subplot(122)
    plt.plot(reach,kth_nondestroyed_register_percentage,'-b*',label=f"1st nondestroyed register percentage")

    k = 5
    for i in range(len(reach)):
      print(reach[i])
      d = self.simulate_one_case(a, m, reach[i],k, trails)
      kth_inactive_register_percentage[i] = d['kth_inactive_register_percentage']
      kth_nondestroyed_register_percentage[i] = d['kth_nondestroyed_register_percentage']
      expected_active_register_pecentage[i] = s.legions_expectation(reach[i]/m)*100
    plt.subplot(121)
    plt.plot(reach,kth_inactive_register_percentage,'-m*',label=f"{k}th inactive register percentage")
    plt.subplot(122)
    plt.plot(reach,kth_nondestroyed_register_percentage,'-m*',label=f"{k}th nondestroyed register percentage")

    k = 20
    for i in range(len(reach)):
      print(reach[i])
      d = self.simulate_one_case(a, m, reach[i],k, trails)
      kth_inactive_register_percentage[i] = d['kth_inactive_register_percentage']
      kth_nondestroyed_register_percentage[i] = d['kth_nondestroyed_register_percentage']
      expected_active_register_pecentage[i] = s.legions_expectation(reach[i]/m)*100
    plt.subplot(121)
    plt.plot(reach,kth_inactive_register_percentage,'-c*',label=f"{k}th inactive register percentage")
    plt.subplot(122)
    plt.plot(reach,kth_nondestroyed_register_percentage,'-c*',label=f"{k}th nondestroyed register percentage")

    k = 100
    for i in range(len(reach)):
      print(reach[i])
      d = self.simulate_one_case(a, m, reach[i],k, trails)
      kth_inactive_register_percentage[i] = d['kth_inactive_register_percentage']
      kth_nondestroyed_register_percentage[i] = d['kth_nondestroyed_register_percentage']
      expected_active_register_pecentage[i] = s.legions_expectation(reach[i]/m)*100
    plt.subplot(121)
    plt.plot(reach,kth_inactive_register_percentage,'-g*',label=f"{k}th inactive register percentage")
    plt.subplot(122)
    plt.plot(reach,kth_nondestroyed_register_percentage,'-g*',label=f"{k}th nondestroyed register percentage")



    plt.subplot(121)
    plt.plot(reach,expected_active_register_pecentage,'-r*',label='expected_active_register_pecentage')
    plt.legend(loc='upper left', shadow=True)
    plt.grid(True)
    plt.xscale('log')
    plt.xlabel('reach')
    plt.subplot(122)
    plt.plot(reach,expected_active_register_pecentage,'-r*',label='expected_active_register_pecentage')
    plt.legend(loc='upper left', shadow=True)
    plt.grid(True)
    plt.xscale('log')
    plt.xlabel('reach')

    plt.show()



if __name__ == '__main__':
  absltest.main()
